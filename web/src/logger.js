import Config from 'Root/config';

export const DEBUG = 0;
export const INFO = 1;
export const WARN = 2;
export const ERROR = 3;

function printLog(logLevel, message) {
  console.log(`${new Date().toISOString()} [${logLevel}] ${message}`);
}

class Logger {
  constructor() {
    this.logLevel = Config.logLevel;
  }
  setLogLevel(level) {
    this.logLevel = level;
  }
  debug(message) {
    if (this.logLevel <= DEBUG) {
      printLog('DEBUG', message);
    }
  }
  info(message) {
    if (this.logLevel <= INFO) {
      printLog('INFO', message);
    }
  }
  warn(message) {
    if (this.logLevel <= WARN) {
      printLog('WARN', message);
    }
  }
  error(message) {
    if (this.logLevel <= ERROR) {
      printLog('ERROR', message);
    }
  }
}

const logger = new Logger();
export {logger};
