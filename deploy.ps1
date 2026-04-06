param(
    [Parameter(Position=0)]
    [ValidateSet("help", "build", "up", "down", "logs", "clean", "dev", "prod", "status", "restart", "backend", "frontend", "install", "run-backend", "run-frontend")]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "Available commands:" -ForegroundColor Cyan
    Write-Host "help          - Show this help message" -ForegroundColor White
    Write-Host "build         - Build all Docker containers" -ForegroundColor White
    Write-Host "up            - Start all services" -ForegroundColor White
    Write-Host "down          - Stop all services" -ForegroundColor White
    Write-Host "logs          - Show logs for all services" -ForegroundColor White
    Write-Host "clean         - Remove all containers and images" -ForegroundColor White
    Write-Host "dev           - Start development environment" -ForegroundColor White
    Write-Host "prod          - Start production environment" -ForegroundColor White
    Write-Host "status        - Show status of all services" -ForegroundColor White
    Write-Host "restart       - Restart all services" -ForegroundColor White
    Write-Host "backend       - Start only backend service" -ForegroundColor White
    Write-Host "frontend      - Start only frontend service" -ForegroundColor White
    Write-Host "install       - Install dependencies locally" -ForegroundColor White
    Write-Host "run-backend   - Run backend locally" -ForegroundColor White
    Write-Host "run-frontend  - Run frontend locally" -ForegroundColor White
}

function Start-Dev {
    Write-Host "Starting development environment..." -ForegroundColor Yellow
    docker-compose up --build
}

# Execute command
switch ($Command) {
    "help" { Show-Help }
    "dev" { Start-Dev }
    default { 
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Show-Help
    }
}
