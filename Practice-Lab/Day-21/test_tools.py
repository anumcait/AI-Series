from tools import (
    calculate,
    get_server_status,
    get_disk_usage,
    check_service
)


print("Calculator:")
print(calculate("45 * 27"))


print("\nServer Status:")
print(get_server_status("production"))


print("\nDisk Usage:")
print(get_disk_usage("production"))


print("\nService Status:")
print(
    check_service(
        "production",
        "nginx"
    )
)