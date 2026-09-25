from django.db import models

class Table(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Available'
        OCCUPIED = 'OCCUPIED', 'Occupied'
        RESERVED = 'RESERVED', 'Reserved'

    number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField(default=4)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE
    )

    class Meta:
        ordering = ['number']

    def is_available(self):
        return self.status == self.Status.AVAILABLE

    def mark_occupied(self):
        self.status = self.Status.OCCUPIED
        self.save()

    def mark_reserved(self):
        self.status = self.Status.RESERVED
        self.save()

    def mark_available(self):
        self.status = self.Status.AVAILABLE
        self.save()

    def __str__(self):
        return f"Table {self.number} ({self.capacity} Seats) - {self.get_status_display()}"
