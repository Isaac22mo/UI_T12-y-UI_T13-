from django.db import models

class ErrorLog(models.Model):
    #Es igual a poner varchar(10)
    codigo = models.CharField(max_length=10),
    #Es igual a lonText
    mensaje = models.TextField(),
    #Es igual Date(now))
    fecha = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return f"{self.codigo} - {self.mensaje}"

