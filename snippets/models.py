from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

# Prepare pygments library.
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

# Begin Models.
class Snippet(models.Model):
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlihted = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linones = models.BooleanField(default=False)
    langauge = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """

        lexer = get_lexer_by_name(self.langauge)
        linones = 'table' if self.linones else False
        options = {'title': self.title} if self.title else{}
        formatter = HtmlFormatter(style=self.style, linones=linones, full=True, **options)
        self.highlihted = highlight(self.code, lexer, formatter)
        
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('created',)

