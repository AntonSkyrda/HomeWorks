from django import forms
from .models import Task, TaskAnswer


class TaskAnswerForm(forms.ModelForm):
    class Meta:
        model = TaskAnswer
        fields = [
            "task",
            "description",
        ]

    task = forms.ModelChoiceField(
        queryset=Task.objects.all(),
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Your answer here...", "rows": 4, "cols": 40}
        ),
        label="Answer Description",
        required=True,
    )

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if len(description) < 10:
            raise forms.ValidationError(
                "Answer description must be at least 10 characters."
            )
        return description
