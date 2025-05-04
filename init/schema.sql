CREATE TABLE IF NOT EXISTS oc_customer (
  customer_id INT AUTO_INCREMENT PRIMARY KEY,
  firstname VARCHAR(32),
  lastname VARCHAR(32),
  email VARCHAR(96) UNIQUE,
  telephone VARCHAR(32),
  password VARCHAR(255),
  newsletter TINYINT(1),
  status TINYINT(1),
  date_added DATETIME
);
