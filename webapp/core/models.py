"""Data models for the skill-gap analyzer knowledge domain."""

from django.db import models


class Skill(models.Model):
    """A skill that can be associated with a role or learning resource."""

    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    category = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Role(models.Model):
    """A target job role and its required skills."""

    name = models.CharField(max_length=160, unique=True)
    slug = models.SlugField(max_length=180, unique=True)
    description = models.TextField(blank=True)
    required_skills = models.ManyToManyField(Skill, through="RoleSkill", related_name="roles")

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class RoleSkill(models.Model):
    """Associates a skill with a role and records its importance."""

    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    importance = models.PositiveSmallIntegerField(default=3)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["role", "skill"], name="unique_role_skill"),
        ]
        ordering = ["role", "-importance", "skill"]


class LearningResource(models.Model):
    """A reviewable resource that may help develop a skill."""

    RESOURCE_TYPES = [
        ("course", "Course"),
        ("documentation", "Documentation"),
        ("book", "Book"),
        ("practice", "Practice"),
    ]

    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="learning_resources")
    title = models.CharField(max_length=200)
    url = models.URLField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["skill", "title"]

    def __str__(self) -> str:
        return self.title
