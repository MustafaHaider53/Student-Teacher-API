from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, role ,name ,  password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            role=role,
            name=name,
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, role , password=None):
        
        user = self.create_user(
            email,
            password=password,
            role = role,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Create your models here.
class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ('teacher' , 'Teacher'),
        ('student' , 'Student')
    )
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=15 , choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['password' , 'role']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    

class Assingment(models.Model):
    title = models.CharField(max_length=255)
    illustration = models.TextField()
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_assignments'
    )
    assigned_to = models.ForeignKey(  # One student per assignment
        User,
        on_delete=models.CASCADE,
        related_name='assigned_assignments',
    )

    def __str__(self):
        return self.title
    
    


class Submission(models.Model):
    assingment = models.OneToOneField(Assingment , on_delete=models.CASCADE , related_name='submission')
    submit_by = models.ForeignKey(User , on_delete=models.CASCADE , related_name='submission_by')
    solution = models.TextField()

    def __str__(self):
        return self.solution


class Grade(models.Model):
    assingment = models.OneToOneField(Assingment , on_delete=models.CASCADE , related_name='grade')
    graded_by = models.ForeignKey(User , on_delete=models.CASCADE , related_name='grades_given')
    graded_to = models.ForeignKey(User , on_delete=models.CASCADE ,  related_name='grades_recived')
    grades = models.IntegerField()

    def __str__(self):
        return self.grades

    
    