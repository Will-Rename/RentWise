from App.main import create_app

app = create_app()

# Run a single CLI command and report success or failure
def run_cli_command(*args):
    runner = app.test_cli_runner()
    result = runner.invoke(args=list(args))

    print(f"\n$ flask {' '.join(args)}")
    print(result.output.strip())

    if result.exit_code == 0:
        print("✅ Success")
    else:
        print("❌ Failed")
    
    return result.exit_code == 0  # Returns True if successful

def test_all_cli_commands():
    total = 0
    passed = 0

    def test(*args):
        nonlocal total, passed
        total += 1
        if run_cli_command(*args):
            passed += 1

    # Initialize database
    test("init")

    # User Commands
    test("user", "create", "--default")
    test("user", "create", "--name", "TestUser", "--email", "test@example.com", "--password", "testpass123", "--type", "tenant")
    test("user", "list")

    # Auth Commands
    test("auth", "create-admin", "--default")

    # Tenant Commands
    test("tenant", "create", "--name", "TestTenant", "--email", "tenant@example.com", "--password", "tenantpass123", "--apartment-id", "1")

    # Landlord Commands
    test("landlord", "create", "--name", "TestLandlord", "--email", "landlord@example.com", "--password", "landlordpass123", "--phone", "1234567890")

    # Amenity Commands
    test("amenity", "create", "--default")
    test("amenity", "create", "--name", "TestAmenity")
    test("amenity", "list")
    test("amenity", "get", "--id", "1")
    test("amenity", "delete", "--id", "1")

    # Apartment Commands
    test("apartment", "create",
        "--landlord-id", "1",
        "--name", "Test Apartment",
        "--location", "Test Location",
        "--units-available", "5",
        "--units-total", "10",
        "--details", "Test apartment details"
    )
    test("apartment", "list")
    test("apartment", "list", "--landlord-id", "1")
    test("apartment", "update",
        "--landlord-id", "1",
        "--apartment-id", "1",
        "--name", "Updated Apartment",
        "--location", "Updated Location",
        "--units-available", "4",
        "--units-not-available", "6",
        "--details", "Updated details"
    )
    test("apartment", "add-amenity",
        "--apartment-id", "1",
        "--amenity-id", "1",
        "--landlord-id", "1",
        "--quantity", "2"
    )
    test("apartment", "list-amenities", "--apartment-id", "1")
    test("apartment", "remove-amenity",
        "--apartment-id", "1",
        "--amenity-id", "1",
        "--landlord-id", "1"
    )
    test("apartment", "delete",
        "--landlord-id", "1",
        "--apartment-id", "1"
    )

    # Search Commands
    test("search", "apartments", "--location", "Test Location")
    test("search", "apartments", "--amenity", "TestAmenity")
    test("search", "apartments", "--location", "Test Location", "--amenity", "TestAmenity")

    # Review Commands
    test("review", "create",
        "--tenant-id", "1",
        "--apartment-id", "1",
        "--review-text", "Great apartment!"
    )
    test("review", "list", "--apartment-id", "1")
    test("review", "list", "--tenant-id", "1")
    test("review", "delete",
        "--tenant-id", "1",
        "--review-id", "1"
    )

    # Test Commands
    test("test", "user", "unit")
    test("test", "user", "int")
    test("test", "user", "all")

    print("\nSummary:")
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")

if __name__ == "__main__":
    test_all_cli_commands()
