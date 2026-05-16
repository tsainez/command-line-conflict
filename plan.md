1. **Analyze UX in `SettingsScene`**: The Settings menu lacks audio feedback on hover and keyboard navigation, unlike the `MenuScene`. This causes a lack of immediate tactile confirmation for the user, lowering the perceived responsiveness and accessibility of the UI.
2. **Implement audio feedback**: Instantiate a local `SoundSystem` in `SettingsScene` and trigger `click_select` on mouse hover changes and keyboard up/down presses.
3. **Enhance volume adjustment feedback**: When users adjust Master or SFX volume, update the volume of the `SoundSystem` on the fly and play a sound so they can instantly hear the result of their change.
4. **Update `.Jules/palette.md`**: Log this critical learning about UI consistency and audio feedback in Pygame non-ECS scenes.
5. **Pre-commit and Test**: Verify the implementation with tests and linting.
6. **Submit**: Create PR.
