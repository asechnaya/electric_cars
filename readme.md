Запуск ```pytest -v --tb=line```

Тест-кейсы: test_cases.xlsx

Найденные баги: 

1) Ошибка при ускорении до 100%
2) Остаточные напряжения при ошибке в работе мотора
3) Возможность переключить передачу (подать напряжение на gear 1, 2) при моторе в состоянии NotReady
4) Разрешено переключение передачи при отказе тормозов

Пример оформления баг-репорта: папка bug-reports