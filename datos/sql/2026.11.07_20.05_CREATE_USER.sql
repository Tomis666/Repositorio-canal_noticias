CREATE USER IF NOT EXISTS 'canal_noticias'@'localhost' IDENTIFIED BY 'canal2026';

GRANT ALL PRIVILEGES ON canal_noticias.* TO 'canal_noticias'@'localhost';

FLUSH PRIVILEGES;
