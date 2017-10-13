export const DEBUG = 0;
export const INFO = 1;
export const WARN = 2;
export const ERROR = 3;

const LOG_LEVELS = ['DEBUG', 'INFO', 'WARN', 'ERROR'];

function printLog(logLevel, message) {
  console.log(`${new Date().toISOString()} [${LOG_LEVELS[logLevel]}] ${message}`);
}

class Logger {
  constructor() {
    // todo: change to INFO for production
    this.logLevel = DEBUG;
  }
  setLogLevel(level) {
    this.logLevel = level;
  }
  debug(message) {
    if (this.logLevel <= DEBUG) {
      printLog(this.logLevel, message);
    }
  }
  info(message) {
    if (this.logLevel <= INFO) {
      printLog(this.logLevel, message);
    }
  }
  warn(message) {
    if (this.logLevel <= WARN) {
      printLog(this.logLevel, message);
    }
  }
  error(message) {
    if (this.logLevel <= ERROR) {
      printLog(this.logLevel, message);
    }
  }
}

const logger = new Logger();
export {logger};
