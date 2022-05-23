from django.db import models

class Robot(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class RobotProcess(models.Model):
    name = models.CharField(max_length=100)    
    status = models.CharField(max_length=100, choices=[('running', 'running'), ('stopped', 'stopped')])
    success = models.BooleanField(default=False)
    error = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    

class ProcessLog(models.Model):
    process = models.ForeignKey(RobotProcess, on_delete=models.CASCADE)
    log_type = models.CharField(max_length=100, choices=[('info', 'info'), ('error', 'error')])
    message = models.CharField(max_length=100)
    hostname = models.CharField(max_length=100)
    cpu_usage = models.FloatField()
    cpu_total = models.FloatField()
    ram_usage = models.FloatField()
    ram_total = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.process.name} - {self.log_type} - {self.message}"
    
    class Meta:
        ordering = ['-created_at', '-process__created_at']
    
