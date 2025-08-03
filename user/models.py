from django.db import models
from django.contrib.auth.hashers import make_password
from django.db import models

PICKUP_CHOICES = [
    ('Кара-Балта', 'Кара-Балта'),
    ('Сокулук', 'Сокулук'),
    ('Беловодское', 'Беловодское'),
]

PREFIX_MAP = {
  'Кара-Балта': 'AKB',
  'Сокулук': 'ASK',
  'Беловодское': 'AUN',
}

class User(models.Model):
    phone_number = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)  # обычный текст
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    pickUpPoint = models.CharField(max_length=100, choices=PICKUP_CHOICES)
    warehouse = models.TextField(blank=True)
    client_id = models.CharField(max_length=255, blank=True, unique=True)

    def save(self, *args, **kwargs):
        # Генерация client_id
        if not self.client_id:
            prefix = PREFIX_MAP.get(self.pickUpPoint)
            last_user = User.objects.filter(client_id__startswith=prefix).order_by('-id').first()
            last_number = 0
            if last_user and last_user.client_id:
                try:
                    last_number = int(last_user.client_id.replace(prefix, ''))
                except ValueError:
                    pass
            self.client_id = f'{prefix}{last_number + 1:03}'

        # Генерация warehouse
        self.warehouse = (
            f"姓名:{self.name}{self.client_id}，电话：{self.phone_number}， "
            f"адрес: 广东省佛山市南海区里水镇海南洲工业区53号至和贸易（{self.client_id}）仓库 "
            f"代码: AUN-1999({self.phone_number}) {self.client_id}"
        )

        super().save(*args, **kwargs)