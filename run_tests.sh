#!/bin/bash

# Test Runner Script for Course Enrollment API

echo "========================================="
echo "Course Enrollment API - Test Suite"
echo "========================================="
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "Warning: Virtual environment not activated"
    echo "Run: source venv/bin/activate"
    echo ""
fi

# Run all tests with verbose output
echo "Running all tests..."
echo ""
pytest -v

echo ""
echo "========================================="
echo "Test Results Summary"
echo "========================================="
echo ""

# Run tests with coverage
echo "Running tests with coverage..."
echo ""
pytest --cov=app --cov-report=term-missing

echo ""
echo "========================================="
echo "All tests complete!"
echo "========================================="
