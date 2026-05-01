from LogDatabase import LogDatabase

log_database = LogDatabase()
log_database.storeNumLogs(0)

# storeBlock, fetchBlock, eraseBlock tests
test_addr = 0x010
test_data = [10, 20, 30, 40]

log_database.storeBlock(test_addr, test_data)
print("Stored Block:", test_data)

fetched = log_database.fetchBlock(test_addr, len(test_data))
print("Fetched Block:", fetched)

log_database.eraseBlock(test_addr, len(test_data))
erased = log_database.fetchBlock(test_addr, len(test_data))
print("Erased Block:", erased)

# createLog test
log = log_database.createLog(256.0)
print("Created Log:", log)

# fetchNumLogs and incrementNumLogs tests
num_logs_before = log_database.fetchNumLogs()
print("Num Logs (Before):", num_logs_before)

log_database.incrementNumLogs()

num_logs_after = log_database.fetchNumLogs()
print("Num Logs (After):", num_logs_after)

# storeLog and fetchLog tests
log_database.storeLog(log_database.createLog(50.0))
log_database.storeLog(log_database.createLog(100.0))

logs = log_database.fetchLogs()
print("All Logs:", logs)