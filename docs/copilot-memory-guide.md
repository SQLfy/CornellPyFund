# GitHub Copilot Memory Feature

## Overview

This repository is configured to use GitHub Copilot with the memory feature enabled. This allows Copilot to remember context from your conversations and provide more personalized assistance.

## How to Turn On Memory in GitHub Copilot

The memory feature is already enabled in this repository's devcontainer configuration. When you open this project in VS Code using the dev container, GitHub Copilot will automatically have memory enabled.

### Configuration Details

The following settings are configured in `.devcontainer/devcontainer.json`:

1. **GitHub Copilot Extensions**: 
   - `github.copilot` - Main Copilot extension
   - `github.copilot-chat` - Copilot Chat extension with memory capabilities

2. **Memory Setting**:
   - `github.copilot.chat.memory.enabled: true` - Enables the memory feature

### What Does Memory Do?

With memory enabled, GitHub Copilot can:
- Remember previous conversations within your session
- Understand project-specific context over time
- Provide more relevant suggestions based on your coding patterns
- Recall information you've shared in previous chats

### Using the Memory Feature

1. **Start a conversation**: Open GitHub Copilot Chat (Ctrl+Shift+I or Cmd+Shift+I)
2. **Share context**: Tell Copilot about your project, coding preferences, or specific requirements
3. **Continue working**: Copilot will remember this context in future interactions
4. **Review memory**: You can ask Copilot what it remembers about your project

### Manual Configuration (For Non-Devcontainer Environments)

If you're not using the devcontainer, you can enable memory manually:

1. Open VS Code Settings (Ctrl+, or Cmd+,)
2. Search for "github.copilot.chat.memory.enabled"
3. Check the box to enable memory
4. Restart VS Code for changes to take effect

Alternatively, add this to your `settings.json`:

```json
{
  "github.copilot.chat.memory.enabled": true,
  "github.copilot.chat.useProjectTemplates": true
}
```

## Privacy and Data

- Memory is stored locally and session-based
- No conversation data is permanently stored unless explicitly saved
- You can clear memory by restarting VS Code or clearing chat history

## Troubleshooting

### Memory Not Working?

1. Ensure you have the latest version of GitHub Copilot extensions
2. Check that your GitHub Copilot subscription is active
3. Verify the setting in VS Code: File > Preferences > Settings > Search "copilot memory"
4. Try reloading the VS Code window: Ctrl+Shift+P > "Developer: Reload Window"

### Need to Reset Memory?

- Close and reopen VS Code
- Or use the command palette: Ctrl+Shift+P > "GitHub Copilot: Reset Memory"

## Additional Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [VS Code GitHub Copilot Extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
- [GitHub Copilot Chat Extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat)
