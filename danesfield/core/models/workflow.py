from __future__ import annotations
from typing import List

from django.contrib.postgres.fields import ArrayField

from django.db import models
from django.db.models.aggregates import Count
from django_extensions.db.models import TimeStampedModel


class WorkflowStepDependency(TimeStampedModel):
    """
    A dependency relation between two workflow steps.

    This uses a closure table design, and supports trees of connected workflow steps.
    In this model, parent points to any step that must run before the corresponding child step.
    In any given workflow, a WorkflowStep will have multiple corresponding WorkflowStepDependency
    entries pointing to it, to indicate the steps which run before and after it (e.g. where on
    the tree it resides). There is an entry in this table for any dependency, not just immediate.
    For example, if there is a workflow of the following format:

        A -> B -> C

    There will be connections from A to B, A to C, and B to C. For each workflow step, there is
    also a self referencing connection (e.g. for step A, parent = A, child = A), to ensure consistency.
    NOTE: This model should not be instantiated directly, as creating objects incorrectly can cause
    inconsistencies. Rather, the provided methods in Workflow and WorkflowStep should be used.
    """

    parent = models.ForeignKey(
        'WorkflowStep', related_name='workflow_step_parents', on_delete=models.CASCADE
    )
    child = models.ForeignKey(
        'WorkflowStep', related_name='workflow_step_children', on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['parent', 'child'], name='unique_dependency')
        ]


class WorkflowStep(TimeStampedModel):
    """An algorithm to run in a workflow."""

    name = models.CharField(max_length=255)
    # docker_image = models.ForeignKey(??)
    invocation = ArrayField(models.CharField(max_length=255))
    workflow = models.ForeignKey(
        'Workflow', related_name='workflow_steps', on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['workflow', 'name'], name='unique_workflow_step')
        ]

    def parents(self) -> List[WorkflowStep]:
        """Return all parents of this step (all steps that run prior to this step)."""
        return [
            relation.parent
            for relation in WorkflowStepDependency.objects.filter(child=self)
            .exclude(parent=self)
            .select_related('parent')
        ]

    def children(self) -> List[WorkflowStep]:
        """Return all children of this step (all steps that run after this step)."""
        return [
            relation.child
            for relation in WorkflowStepDependency.objects.filter(parent=self)
            .exclude(child=self)
            .select_related('parent')
        ]

    def append_step(self, step: WorkflowStep):
        """Add a step to the workflow, running after this step."""
        # Ensure that step is saved
        step.save()

        # Create dependencies between this step's parents and the new step
        dependencies = [WorkflowStepDependency(parent=a, child=step) for a in self.parents()]

        # Create a dependency between this step and the new step
        dependencies.append(WorkflowStepDependency(parent=self, child=step))

        # Add self reference dependency
        dependencies.append(WorkflowStepDependency(parent=step, child=step))

        # Save dependencies
        WorkflowStepDependency.objects.bulk_create(dependencies)

        # Return added step
        return step


# TODO: Add signals for workflow step post_save, to add self referencing paths
# Assume that any workflow steps that are created on their own, are root steps


class Workflow(TimeStampedModel):
    """A model for organizing the running of workflow steps."""

    name = models.CharField(max_length=255, unique=True)
    # TODO: Add more fields

    def steps(self) -> List[WorkflowStep]:
        """
        Return all workflow steps, ordered from first to last.

        This function returns the steps in Bread First Search (BFS) ordering.
        """
        # Get all steps, ordering from most to least parent dependencies (first run to last run)
        all_steps = (
            WorkflowStep.objects.filter(workflow=self)
            .annotate(count=Count('workflow_step_parents'))
            .order_by('-count')
        )

        return list(all_steps)

    def add_root_step(self, workflow_step: WorkflowStep) -> WorkflowStep:
        """
        Add a step to run at the beginning of a workflow.

        Note: There is not necessarily a single root step, and as such multiple steps
        can run at the beginning of a workflow.
        """
        # Ensure step is saved
        workflow_step.save()

        # Add self referencing step
        WorkflowStepDependency.objects.create(parent=workflow_step, child=workflow_step)

        # Return added_step
        return workflow_step
