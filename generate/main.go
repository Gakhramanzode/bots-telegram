package main

import (
	"log"
	"math/rand"
	"os"
	"strconv"
	"strings"

	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func main() {
	// Response telegram bot token
	token := os.Getenv("GENERATE_BOT_TOKEN")
	if token == "" {
		log.Fatal("GENERATE_BOT_TOKEN environment variable is not set")
	}

	// Initialize the bot
	bot, err := tgbotapi.NewBotAPI(token)
	if err != nil {
		log.Panic(err)
	}

	log.Printf("Authorized on account %s", bot.Self.UserName)

	// Subscribe to updates
	u := tgbotapi.NewUpdate(0)
	u.Timeout = 60

	updates := bot.GetUpdatesChan(u)

	// Main loop
	for update := range updates {
		if update.Message != nil && update.Message.IsCommand() {
			switch update.Message.Command() {
			case "start":
				log.Println("Command /start received")

				// Send a welcome message to the user
				msg := tgbotapi.NewMessage(update.Message.Chat.ID,
					"Hello! I am a bot that can generate random names and passwords. Use the /generate_nickname command to generate a name or the /generate_password command to generate a password.")

				bot.Send(msg)

			case "generate_pin":
				log.Println("Command /generate_pin received")

				// Call the PIN generation function
				pin := generatePIN()

				// Send the generated PIN to the user with Markdown formatting
				text := "Your random pin number:\n```\n" + pin + "\n```"
				msg := tgbotapi.NewMessage(update.Message.Chat.ID, text)
				msg.ParseMode = "MarkdownV2"

				bot.Send(msg)

			case "generate_nickname":
				log.Println("Command /generate_nickname received")

				// Call the nickname generation function
				nickname := generateNickname()

				// Send the generated nickname to the user with Markdown formatting
				text := "Your random nickname:\n```\n" + nickname + "\n```"
				msg := tgbotapi.NewMessage(update.Message.Chat.ID, text)
				msg.ParseMode = "MarkdownV2"

				bot.Send(msg)

			case "generate_port_number":
				log.Println("Command /generate_port_number received")

				// Call the port number generation function
				port := generatePortNumber()

				// Send the generated port number to the user witch Markdown formatting
				text := "Your random port number:\n```\n" + strconv.Itoa(port) + "\n```"
				msg := tgbotapi.NewMessage(update.Message.Chat.ID, text)
				msg.ParseMode = "MarkdownV2"

				bot.Send(msg)

			case "generate_password":
				log.Println("Command /generate_password received")

				// Call the password generation function
				password := generatePassword(18)
				escaped := escapeMarkdownV2(password)

				// Send the generated password to the user with Markdown formatting
				text := "Your random password:\n```\n" + escaped + "\n```"
				msg := tgbotapi.NewMessage(update.Message.Chat.ID, text)
				msg.ParseMode = "MarkdownV2"

				bot.Send(msg)
			}
		}
	}
}

// PIN generation logic
func generatePIN() string {
	// Generate a random 4-digit PIN
	pin := ""
	for i := 0; i < 4; i++ {
		digit := rand.Intn(10) // Generate a random digit between 0 and 9
		pin += strconv.Itoa(digit)
	}
	return pin
}

// Nickname generation logic
func generateNickname() string {
	// List words to use for nickname generation
	adjectives := []string{
		"adorable", "adventurous", "amazing", "ambitious", "amusing", "awesome", "brave", "bright", "calm", "charming",
		"cheerful", "clever", "confident", "creative", "daring", "delightful", "determined", "eager", "energetic", "enthusiastic",
	}
	animals := []string{
		"alligator", "antelope", "armadillo", "baboon", "badger", "bat", "bear", "beaver", "bee", "bison",
		"boar", "buffalo", "butterfly", "camel", "cat", "cheetah", "chicken", "chimpanzee", "cow", "coyote",
	}

	adjective := adjectives[rand.Intn(len(adjectives))]
	animal := animals[rand.Intn(len(animals))]
	return adjective + "_" + animal
}

// Port number generation logic
func generatePortNumber() int {
	// Generate a random port number between 49152 and 65535
	port := rand.Intn(65536-49152+1) + 49152
	return port
}

// Function to escape special characters in Markdown V2
func escapeMarkdownV2(text string) string {
	// List of special characters in Markdown V2
	// https://core.telegram.org/bots/api#markdownv2-style
	special := "\\_*[]()~`>#+-=|{}.!"
	escaped := ""

	// Escape special characters
	for _, char := range text {
		if strings.ContainsRune(special, char) {
			escaped += "\\" + string(char)
		} else {
			escaped += string(char)
		}
	}
	return escaped
}

// Function to generate a random password
func generatePassword(length int) string {
	// Seed the random number generator
	letters := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	digits := "0123456789"
	punctuation := `!"#$%&'()*+,-./:;<=>?@[\]^_{|}~`
	all := letters + digits + punctuation

	// Generate a random password
	var password strings.Builder
	for i := 0; i < length; i++ {
		index := rand.Intn(len(all))
		password.WriteByte(all[index])
	}
	return password.String()
}
