import pytest

from danesfield.core.models.workflow import Workflow, WorkflowStep


@pytest.mark.django_db
def test_workflow_step_create():
    workflow: Workflow = Workflow.objects.create(name='test')
    workflow.add_root_step(WorkflowStep(workflow=workflow, name='initial_step', invocation=[]))

    workflow_steps = workflow.steps()
    assert len(workflow_steps) == 1

    step = workflow_steps[0]
    assert step.name == 'initial_step'
    assert step.workflow == workflow


@pytest.mark.django_db
def test_workflow_step_append():
    workflow: Workflow = Workflow.objects.create(name='test')
    workflow.add_root_step(WorkflowStep(workflow=workflow, name='initial_step', invocation=[]))

    root_step = workflow.steps()[0]
    root_step.append_step(
        WorkflowStep(workflow=workflow, name='second_step', invocation=['foo', 'bar'])
    )

    workflow_steps = workflow.steps()
    assert len(workflow_steps) == 2

    parent_step, child_step = workflow_steps
    assert child_step.ancestors() == [parent_step]


@pytest.mark.django_db
def test_workflow_step_append_2():
    workflow: Workflow = Workflow.objects.create(name='test')
    workflow.add_root_step(WorkflowStep(workflow=workflow, name='initial_step', invocation=[]))

    root_step = workflow.steps()[0]
    step_2: WorkflowStep = WorkflowStep.objects.create(
        workflow=workflow, name='second_step', invocation=['foo', 'bar']
    )
    root_step.append_step(step_2)

    step_3: WorkflowStep = WorkflowStep.objects.create(
        workflow=workflow, name='third_step', invocation=[]
    )
    step_2.append_step(step_3)

    # Assert that ordering is correct
    workflow_steps = workflow.steps()
    assert [root_step.pk, step_2.pk, step_3.pk] == [step.pk for step in workflow_steps]

    # TODO: Move below to its own test

    # Add another child step to step 2
    step_4: WorkflowStep = WorkflowStep.objects.create(
        workflow=workflow, name='fourth_step', invocation=[]
    )
    step_2.append_step(step_4)

    # Add another child to step 3
    step_5: WorkflowStep = WorkflowStep.objects.create(
        workflow=workflow, name='fifth_step', invocation=[]
    )
    step_3.append_step(step_5)


@pytest.mark.django_db
def test_workflow_step_delete_parent():
    workflow: Workflow = Workflow.objects.create(name='test')

    root_step: WorkflowStep = WorkflowStep.objects.create(
        workflow=workflow, name='initial_step', invocation=[]
    )
    workflow.add_root_step(root_step)

    step_2: WorkflowStep = WorkflowStep.objects.create(
        workflow=workflow, name='second_step', invocation=['foo', 'bar']
    )
    root_step.append_step(step_2)

    # Delete root step
    root_step.delete()
    assert workflow.steps() == [step_2]


@pytest.mark.django_db
def test_workflow_step_delete_child():
    workflow: Workflow = Workflow.objects.create(name='test')

    root_step: WorkflowStep = WorkflowStep.objects.create(
        workflow=workflow, name='initial_step', invocation=[]
    )
    workflow.add_root_step(root_step)

    step_2: WorkflowStep = WorkflowStep.objects.create(
        workflow=workflow, name='second_step', invocation=['foo', 'bar']
    )
    root_step.append_step(step_2)

    # Delete second step
    step_2.delete()
    assert workflow.steps() == [root_step]
