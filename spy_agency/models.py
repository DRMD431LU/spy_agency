from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class SpyUser(AbstractUser):
    HITMAN = '1'
    BOSS = '2'
    BIGBOSS = '3'
    ACTIVE = 'ACTIVE'
    INACTIVE = 'ACTIVE'
    app_label = 'spy_agency'
    user_type_data = ((HITMAN, "hitman"), (BOSS, "boss"), (BIGBOSS, "bigboss"))
    user_type = models.CharField(choices=user_type_data, max_length=10)
    status_type_data = ((INACTIVE, "INACTIVE"), (ACTIVE, "ACTIVE"))
    status_type = models.CharField(default=ACTIVE, choices=status_type_data, max_length=10)
    
    def __str__(self):
        return self.username


class Hit(models.Model):
    description = models.TextField()
    target = models.CharField(max_length=255)
    creator = models.ForeignKey(SpyUser, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.target


class Assignment(models.Model):
    UNASSIGNED = 'UNASSIGNED'
    ASSIGNED = 'ASSIGNED'
    FAILED = 'FAILED'
    COMPLETED = 'COMPLETED'
    assignee = models.ForeignKey(SpyUser, on_delete=models.SET_NULL, null=True)
    hit = models.OneToOneField(Hit, on_delete=models.SET_NULL, null=True)
    status_type_data = ((UNASSIGNED, "UNASSIGNED"), (ASSIGNED, "ASSIGNED"), (FAILED, "FAILED"), (COMPLETED, "COMPLETED"))
    status_type = models.CharField(default=UNASSIGNED, choices=status_type_data, max_length=10)
    def __str__(self):
        return f'{self.assignee.username} assigned to kill {self.hit.target}'


class HitmanUser(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(SpyUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    def __str__(self):
        return self.admin.username if self.admin.username else self


class BossUser(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(SpyUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.admin.username if self.admin.username else self


class HitmanAssignedBoss(models.Model):
    hitman = models.ForeignKey(HitmanUser, on_delete=models.SET_NULL, null=True)
    boss = models.ForeignKey(BossUser, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f'{self.hitman.admin.username} assigned to {self.boss.admin.username}'


#Creating Django Signals
@receiver(post_save, sender=SpyUser)
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            HitmanUser.objects.create(admin=instance)
        if instance.user_type == 2:
            BossUser.objects.create(admin=instance)

 
@receiver(post_save, sender=SpyUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.hitmanuser.save()
    if instance.user_type == 2:
        instance.bossuser.save()
