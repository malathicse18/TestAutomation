package main

import (
	"fmt"
	"log"
	"net/http"
	"os/exec"

	"github.com/gin-gonic/gin"
)

type CleanupRequest struct {
	Directory string `json:"directory"`
}

func cleanupHandler(c *gin.Context) {
	fmt.Println("✅ Received a cleanup request")

	var request CleanupRequest
	if err := c.ShouldBindJSON(&request); err != nil {
		fmt.Println("❌ Error parsing JSON:", err)
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid JSON"})
		return
	}

	fmt.Println("📂 Directory received:", request.Directory)

	pythonScriptPath := "cleanfiles/cleanup.py" // Update if needed

	// Run Python script
	cmd := exec.Command("python", pythonScriptPath, request.Directory) // For Windows use "python" instead of "python3"
	output, err := cmd.CombinedOutput()

	fmt.Println("🐍 Python Output:", string(output))

	if err != nil {
		fmt.Println("❌ Error executing Python script:", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error(), "output": string(output)})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Cleanup executed", "output": string(output)})
}

func main() {
	router := gin.Default()
	router.POST("/cleanup", cleanupHandler)

	port := "8080"
	fmt.Println("Server running on port", port)
	if err := router.Run(":" + port); err != nil {
		log.Fatal("Failed to start server:", err)
	}
}
