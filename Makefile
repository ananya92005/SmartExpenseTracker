#!/bin/bash
# Common commands for Smart Expense Tracker

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Smart Expense Tracker - Common Commands${NC}"
echo "========================================"
echo ""
echo "Migrations:"
echo "  make migrate          - Run pending migrations"
echo "  make makemigrations   - Create migration files"
echo "  make reset-db         - Reset database (WARNING: deletes all data)"
echo ""
echo "Server:"
echo "  make runserver        - Start development server"
echo "  make shell            - Start Django shell"
echo ""
echo "Testing:"
echo "  make test             - Run all tests"
echo "  make test-verbose     - Run tests with verbose output"
echo ""
echo "Utils:"
echo "  make superuser        - Create superuser"
echo "  make collect-static   - Collect static files"
echo "  make clean            - Clean Python cache files"
echo ""

# Function definitions
migrate() {
    python manage.py migrate
}

makemigrations() {
    python manage.py makemigrations
}

reset_db() {
    echo -e "${YELLOW}⚠️  WARNING: This will delete all data!${NC}"
    read -p "Are you sure? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm db.sqlite3
        python manage.py migrate
        python manage.py createsuperuser
        echo -e "${GREEN}Database reset!${NC}"
    fi
}

runserver() {
    python manage.py runserver
}

shell() {
    python manage.py shell
}

test() {
    python manage.py test
}

test_verbose() {
    python manage.py test -v 2
}

superuser() {
    python manage.py createsuperuser
}

collect_static() {
    python manage.py collectstatic --noinput
}

clean() {
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -name "*.pyc" -delete
    echo -e "${GREEN}Clean completed!${NC}"
}

# Execute command
if [ $# -eq 0 ]; then
    echo "Usage: $0 <command>"
    exit 1
fi

case "$1" in
    migrate)
        migrate
        ;;
    makemigrations)
        makemigrations
        ;;
    reset-db)
        reset_db
        ;;
    runserver)
        runserver
        ;;
    shell)
        shell
        ;;
    test)
        test
        ;;
    test-verbose)
        test_verbose
        ;;
    superuser)
        superuser
        ;;
    collect-static)
        collect_static
        ;;
    clean)
        clean
        ;;
    *)
        echo "Unknown command: $1"
        ;;
esac
