from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    updated = models.DateField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to="post_images")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"post_slug": self.slug})


    class Meta:
        ordering = ["timestamp", "-updated"]

def create_slug(instance, new_slug=None):
    slug = slugify (instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s"%(slug,qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug=create_slug(instance)



pre_save.connect(pre_save_post_reciever,sender=Post)


