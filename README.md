# Habit Tracker

# Obtener token JWT
curl -X POST http://localhost:5000/api/login -H "Content-Type: application/json" -d "{\"email\":\"dvillaj@gmail.com\", \"password\":\"holahola\"}"

# Usar el token en las llamadas
curl http://localhost:5000/api/habits -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczODczNzk0MiwianRpIjoiOWZkZmRlZTUtOWQxZC00OTJiLThhMGEtODc1YWRmNjliY2ExIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3Mzg3Mzc5NDIsImNzcmYiOiJhYmJhOGUxMS0xM2ViLTRjZDQtYjI5MS1iZDQ1MTA3MmQyMzgiLCJleHAiOjE3Mzg3Mzg4NDJ9.edWpL_Ld95HiiK9jh8Us6g0wToah37yOg3Yr4kbbZlM"


https://github.com/sitek94/habit-tracker-app?tab=readme-ov-file