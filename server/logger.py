import smtplib
from email.message import EmailMessage
import email.utils
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler


LOG_SIZE_LIMIT = 50*1024*1024
BACKUP_COUNT = 5

LOADER_LOGGER_NAME = 'loader'
BACKUP_LOGGER_NAME = 'backup'


# Extend handler class to allow SSL(not TLS) connection by overloading the emit() method
class _SslSmtpHandler(SMTPHandler):
    def emit(self, record):
        try:
            port = self.mailport
            if not port:
                port = smtplib.SMTP_SSL_PORT
            smtp = smtplib.SMTP_SSL(self.mailhost, port)
            msg = EmailMessage()
            msg['From'] = self.fromaddr
            msg['To'] = ','.join(self.toaddrs)
            msg['Subject'] = self.getSubject(record)
            msg['Date'] = email.utils.localtime()
            msg.set_content(self.format(record))
            if self.username:
                smtp.login(self.username, self.password)
            smtp.send_message(msg)
            smtp.quit()
        except Exception:
            self.handleError(record)


def create_rotating_file_handler(log_file):
    return RotatingFileHandler(log_file, maxBytes=LOG_SIZE_LIMIT, backupCount=BACKUP_COUNT)


def create_smtp_handler(settings, subject):
    if not isinstance(settings, dict):
        config = {
            'EMAIL_TO_ADDR': settings.EMAIL_TO_ADDR,
            'EMAIL_FROM_ADDR': settings.EMAIL_FROM_ADDR,
            'EMAIL_SMTP_ADDR': settings.EMAIL_SMTP_ADDR,
            'EMAIL_SMTP_PORT': settings.EMAIL_SMTP_PORT,
            'EMAIL_LOGIN': settings.EMAIL_LOGIN,
            'EMAIL_PASSWORD': settings.EMAIL_PASSWORD
        }
    else:
        config = settings
    return _SslSmtpHandler(mailhost=(config['EMAIL_SMTP_ADDR'], config['EMAIL_SMTP_PORT']),
                           fromaddr=config['EMAIL_FROM_ADDR'],
                           toaddrs=[config['EMAIL_TO_ADDR']],
                           subject=subject,
                           credentials=(config['EMAIL_LOGIN'], config['EMAIL_PASSWORD']))


def create_logger(logger_name, log_file, email_handler=None):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(filename)s] [%(levelname)s] %(message)s')

    rfh = create_rotating_file_handler(log_file)
    rfh.setLevel(logging.DEBUG)
    rfh.setFormatter(formatter)
    logger.addHandler(rfh)

    if email_handler is not None:
        email_handler.setLevel(logging.ERROR)
        logger.addHandler(email_handler)

    return logger


def get_loader_logger():
    return logging.getLogger(LOADER_LOGGER_NAME)
