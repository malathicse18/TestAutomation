package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"os/exec"

	"github.com/gin-gonic/gin"
)

type CleanupRequest struct {
	Directory string `json:"directory"`
}

func runCleanup(directory string) (string, error) {
	cmd := exec.Command("python", "file_cleanup_project\\Tasks\\cleanup.py", directory)
	var out bytes.Buffer
	cmd.Stdout = &out
	err := cmd.Run()
	return out.String(), err
}

func cleanupHandler(c *gin.Context) {
	var req CleanupRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request"})
		return
	}

	output, err := runCleanup(req.Directory)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error running cleanup", "details": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Cleanup triggered", "output": output})
}

func logsHandler(c *gin.Context) {
	resp, err := http.Get("http://localhost:5000/logs")
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to fetch logs"})
		return
	}
	defer resp.Body.Close()

	var logs []map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&logs)
	c.JSON(http.StatusOK, logs)
}

func main() {
	r := gin.Default()
	r.POST("/cleanup", cleanupHandler)
	r.GET("/logs", logsHandler)
	r.Run(":8080")
}
