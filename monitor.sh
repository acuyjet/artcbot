until SLACK_BOT_TOKEN="xoxb-224299809441-evQYrNebdwaj8oEGMq8JENeA" python artcslack.py; do
    echo "Slack crashed. Respawning. . ."
    sleep 1
done
