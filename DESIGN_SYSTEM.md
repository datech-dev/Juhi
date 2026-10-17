# Juhi — Product Design System

**Document status:** Proposed v1.0 baseline  
**Product:** Juhi — AI companion for adults  
**Primary platform:** Android-first mobile application  
**Future platforms:** iOS, web, tablet  
**Prepared:** 17 October 2026  
**Owner:** Product Design + Engineering  
**Related document:** `Juhi_AI_Companion_PRD.md`

> **Design-system mission:** Make Juhi feel warm, personal, expressive, culturally fluent, and trustworthy—without confusing an AI persona for a human being or using emotional pressure to drive engagement or spending.

This document defines the product's visual language, interaction patterns, component rules, content style, accessibility requirements, and implementation conventions. It is the baseline for design files, Flutter widgets, QA, and future platform adaptations. Where implementation details are not yet validated, the specifications below are the proposed defaults and should be tested with users.

---

## 1. Design principles

### 1.1 Warmth without manipulation

Use welcoming colors, generous spacing, human-readable language, and expressive illustrations. Do not use guilt, possessive pressure, fake emergencies, simulated distress, or “you abandoned me” messaging to bring people back or sell credits.

### 1.2 Personal, not uncanny

The companion should feel coherent through consistent personality, language, voice, visual identity, and memory. Avoid pretending that generated content is a real photograph, that the AI is a human, or that it has literal needs or feelings.

### 1.3 Conversation is the product

The chat experience is the primary surface. Reading, typing, sending a voice note, viewing media, and resuming a previous topic must all be fast, clear, and predictable. Most secondary features should be reachable without leaving the conversation unnecessarily.

### 1.4 Emotional control belongs to the user

Let users choose relationship style, tone, language, notifications, saved memories, and boundaries. Make mute, pause, block/report, export/delete, and notification controls discoverable. Do not hide these behind multiple layers.

### 1.5 Expressive, but calm

Use gradient, motion, image-led moments, and haptics sparingly. The app should remain comfortable for long conversations and should not resemble a casino or an endless reward loop.

### 1.6 Inclusive by default

Support English, Hindi, Tamil, Hinglish, Tanglish, and future languages. Avoid relying on color alone, use scalable text, allow system font settings, and design for different literacy levels, hands, devices, and connectivity conditions.

### 1.7 Clear commercial boundaries

Price, limits, renewal, credits, and subscription states must be understandable before purchase. Keep subscription prompts away from emotionally sensitive conversation moments and never interrupt a disclosure of distress with a sales message.

---

## 2. Brand foundation

### 2.1 Brand attributes

| Attribute | Design expression | Avoid |
|---|---|---|
| Warm | Soft surfaces, supportive language, gentle contrast | Overly sweet or infantilizing visuals |
| Personal | Chosen persona, user-led customization, remembered preferences | Claiming human identity or hidden surveillance |
| Expressive | Character portraits, media reactions, voice waveforms, subtle motion | Excessive animation and constant attention-grabbing badges |
| Trustworthy | Clear status, transparent privacy and billing, predictable controls | Dark patterns, surprise charges, ambiguous AI disclosure |
| Modern | Strong hierarchy, refined typography, consistent icons | Generic neon sci-fi clichés and crowded screens |
| Culturally fluent | Script support, code-switching, localizable layout | Stereotypes, forced transliteration, assuming one culture fits all |

### 2.2 Recommended visual direction

**Direction name:** *Warm Modern Companion*

Use a deep plum foundation with a warm lavender highlight, a restrained rose accent, and soft neutral surfaces. Keep the interface legible and quiet; reserve saturated gradients for welcome, character creation, and selected expressive moments. In chat, message readability should win over decoration.

The default interface must remain appealing with a character image disabled. Character imagery is a personal preference, not a required part of using the product.

### 2.3 Logo and wordmark

- Wordmark: `Juhi` in a rounded but highly legible typeface; use lowercase or title-case styling consistently once brand exploration is complete.
- Icon concept: a simple abstract spark, overlapping conversational forms, or a soft four-point bloom. Do not rely on a heart icon alone, since Juhi also supports friendship and non-romantic companionship.
- App icon: single strong symbol, high contrast, recognizable at small sizes; do not put tiny text in the icon.
- Clear space: at least the height of the main symbol on all sides.
- Minimum sizes: 24 px for digital brand symbol use; wordmark minimum width 72 px. Validate final artwork at launcher icon sizes.
- Avoid placing the full wordmark over busy character photography.
- Provide monochrome, light-background, dark-background, and small-icon variants.

### 2.4 AI identity disclosure

Use a concise and persistent-but-unobtrusive label in onboarding and companion profile surfaces, for example: **“AI companion”**. Users should not have to infer that Juhi is artificial. Do not add a disclosure to every message if it becomes intrusive, but make the AI identity available in profile and help surfaces.

---

## 3. Design tokens

Tokens are the single source of truth for visual decisions. Components should reference semantic tokens rather than hard-code colors, spacing, radius, or elevation values.

### 3.1 Color palette — primitives

Primitive colors are raw values. Components should normally use semantic tokens in Section 3.2.

#### Core brand

| Token | Hex | Purpose |
|---|---|---|
| `brand.plum.950` | `#24142F` | Deepest brand shade, dark-mode foundations |
| `brand.plum.900` | `#321B43` | Deep brand background |
| `brand.plum.800` | `#48265D` | Strong dark plum |
| `brand.plum.700` | `#5A3175` | Brand deep |
| `brand.plum.600` | `#6B3D8C` | Brand strong |
| `brand.violet.700` | `#5B3DC4` | Accessible violet emphasis |
| `brand.violet.600` | `#6E4AD7` | Primary brand action |
| `brand.violet.500` | `#8062E8` | Hover/active visual accent where contrast permits |
| `brand.violet.300` | `#B8A7F7` | Dark-surface accent |
| `brand.violet.100` | `#EEE8FF` | Soft brand surface |
| `brand.rose.800` | `#9B294D` | Strong rose accent |
| `brand.rose.700` | `#B8335C` | Text-safe rose accent on light surfaces |
| `brand.rose.600` | `#D34B75` | Decorative rose and expressive highlights |
| `brand.rose.300` | `#F2A2B9` | Dark-mode rose accent |
| `brand.rose.100` | `#FFE7EF` | Soft rose surface |

#### Neutrals

| Token | Hex | Purpose |
|---|---|---|
| `neutral.0` | `#FFFFFF` | White |
| `neutral.25` | `#FCFAFD` | Almost-white canvas |
| `neutral.50` | `#F7F4F9` | App background |
| `neutral.100` | `#EFEAF2` | Subtle surface |
| `neutral.200` | `#DDD5E2` | Border / divider |
| `neutral.300` | `#C7BDCE` | Stronger border |
| `neutral.400` | `#A79AAF` | Muted icons/text only where contrast passes |
| `neutral.500` | `#827489` | Secondary text candidate; test contrast by surface |
| `neutral.600` | `#675A6E` | Secondary text |
| `neutral.700` | `#504455` | Strong secondary text |
| `neutral.800` | `#382E3D` | Main dark text |
| `neutral.900` | `#241C29` | Highest-emphasis light-theme text |

#### Status colors

| Token | Hex | Meaning |
|---|---|---|
| `status.success.700` | `#20734B` | Success text/icon |
| `status.success.100` | `#DDF5E8` | Success surface |
| `status.warning.800` | `#8C4D09` | Warning text/icon |
| `status.warning.100` | `#FFF0D3` | Warning surface |
| `status.error.700` | `#B4233D` | Error text/icon |
| `status.error.100` | `#FFE3E7` | Error surface |
| `status.info.700` | `#2459A6` | Information text/icon |
| `status.info.100` | `#E3EEFF` | Information surface |

Status colors must never be communicated through color alone. Add a label, icon, or both. Status palette values should be rechecked in final design-token builds for contrast on every surface.

### 3.2 Semantic color tokens — light theme

| Semantic token | Value | Usage |
|---|---|---|
| `color.background` | `neutral.50` | Main app background |
| `color.surface` | `neutral.0` | Cards, sheets, text field surface |
| `color.surface.subtle` | `neutral.100` | Secondary panels and grouped controls |
| `color.surface.raised` | `neutral.0` | Dialogs, elevated sheets |
| `color.text.primary` | `neutral.900` | Main content |
| `color.text.secondary` | `neutral.600` | Supporting content |
| `color.text.tertiary` | `neutral.500` | Metadata only where contrast passes |
| `color.text.disabled` | `neutral.400` | Disabled content; never for essential information |
| `color.text.onPrimary` | `neutral.0` | Text on primary-filled controls |
| `color.text.link` | `brand.violet.700` | Links and inline actions |
| `color.border.subtle` | `neutral.200` | Hairline dividers |
| `color.border.strong` | `neutral.300` | Input borders, selected outlines |
| `color.border.focus` | `brand.violet.700` | Keyboard/accessibility focus |
| `color.action.primary` | `brand.violet.700` | Primary button and action |
| `color.action.primaryHover` | `brand.violet.800` or approved darker token | Hover on desktop/web |
| `color.action.secondary` | `brand.violet.100` | Secondary action surface |
| `color.action.tertiary` | `transparent` | Low-emphasis action |
| `color.accent.romance` | `brand.rose.700` | Romantic mode accents, optional reactions |
| `color.accent.expressive` | `brand.violet.600` | Expressive moment accents |
| `color.chat.userBubble` | `#E9E1FF` | User message bubble |
| `color.chat.userText` | `#2F2146` | User message text |
| `color.chat.companionBubble` | `neutral.0` | Juhi message bubble |
| `color.chat.companionText` | `neutral.900` | Juhi message text |
| `color.chat.systemSurface` | `neutral.100` | System notes and dates |
| `color.overlay` | `#1D1427` at 48% opacity | Modal scrim |
| `color.divider` | `neutral.200` | Divider |

> **Contrast rule:** Do not assume all text on a brand color is accessible. Verify actual foreground/background pairs to WCAG 2.2 AA (normally 4.5:1 for body text, 3:1 for large text and essential UI graphics). The primary action should use the approved `brand.violet.700` or a darker contrast-tested value with white text—not the lighter decorative violet by default.

### 3.3 Semantic color tokens — dark theme

| Semantic token | Value | Usage |
|---|---|---|
| `color.background` | `#17111C` | Main dark canvas |
| `color.surface` | `#211A28` | Standard card/input surface |
| `color.surface.subtle` | `#2C2334` | Secondary surface |
| `color.surface.raised` | `#34283D` | Dialogs and elevated surfaces |
| `color.text.primary` | `#F8F3FB` | Main content |
| `color.text.secondary` | `#D0C4D8` | Supporting text |
| `color.text.tertiary` | `#B6A8C0` | Metadata where contrast passes |
| `color.text.disabled` | `#887A91` | Disabled content |
| `color.text.onPrimary` | `#FFFFFF` | Text on primary controls |
| `color.text.link` | `#C8B9FF` | Links |
| `color.border.subtle` | `#3C3046` | Dividers and subtle borders |
| `color.border.strong` | `#5C4A68` | Visible outlines |
| `color.border.focus` | `#D2C4FF` | Focus ring |
| `color.action.primary` | `#B8A6FF` | Primary action fill |
| `color.action.primaryText` | `#291B3A` | Text on light-violet fill |
| `color.action.secondary` | `#392D48` | Secondary action surface |
| `color.accent.romance` | `#F2A2B9` | Rose accent |
| `color.chat.userBubble` | `#43335C` | User message bubble |
| `color.chat.userText` | `#FBF7FF` | User message text |
| `color.chat.companionBubble` | `#292130` | Companion message bubble |
| `color.chat.companionText` | `#F8F3FB` | Companion message text |
| `color.chat.systemSurface` | `#302638` | System notes and dates |
| `color.overlay` | `#09060D` at 64% opacity | Modal scrim |

Dark theme should not be produced by simply inverting colors. Preserve hierarchy and ensure media, message bubbles, separators, status labels, and focus indicators remain visible.

### 3.4 Typography

**Recommended font strategy:** Use a modern sans-serif with excellent multi-script coverage. A system UI font stack is acceptable for the first release. Consider Noto Sans families for consistent coverage across Latin, Devanagari, and Tamil when licensing and rendering have been validated. Bundle fonts only when necessary; test text shaping and fallback on real Android devices.

| Token | Size | Line height | Weight | Typical use |
|---|---:|---:|---|---|
| `type.display` | 32 sp | 40 sp | Bold / 700 | Welcome headline, rare hero moments |
| `type.headline.large` | 28 sp | 36 sp | Bold / 700 | Major screen title |
| `type.headline.medium` | 24 sp | 32 sp | SemiBold / 600 | Section title |
| `type.headline.small` | 20 sp | 28 sp | SemiBold / 600 | Screen or card title |
| `type.title.large` | 18 sp | 26 sp | SemiBold / 600 | Card title, dialog title |
| `type.title.medium` | 16 sp | 24 sp | SemiBold / 600 | Subsection title |
| `type.body.large` | 16 sp | 24 sp | Regular / 400 | Primary readable content |
| `type.body.medium` | 14 sp | 21 sp | Regular / 400 | Standard supporting text |
| `type.body.small` | 12 sp | 18 sp | Regular / 400 | Metadata, only if still readable |
| `type.label.large` | 14 sp | 20 sp | Medium / 500 | Important controls |
| `type.label.medium` | 12 sp | 16 sp | Medium / 500 | Chips, compact labels |
| `type.label.small` | 11 sp | 14 sp | Medium / 500 | Limited metadata; never essential content |
| `type.code` | 13 sp | 20 sp | Regular / 400 | IDs, technical diagnostics only |

Typography rules:
- Use `sp` for text sizes on Android and support system font scaling.
- Do not set fixed-height text containers that clip expanded font sizes or Indian scripts.
- Use sentence case for buttons, settings, and labels. Avoid ALL CAPS except short acronyms.
- Keep body copy at 14 sp or above where practical; long-form reading should default to 16 sp.
- Avoid ultra-light weights. Never use letter spacing as a substitute for hierarchy.
- Use typographic hierarchy before adding extra colors or dividers.
- Confirm glyph coverage for Tamil, Hindi, emoji, combining marks, and mixed-script messages.

### 3.5 Spacing scale

Base unit: **4 dp**. Apply only scale values unless a documented exception improves layout.

| Token | Value | Typical use |
|---|---:|---|
| `space.0` | 0 dp | Flush elements |
| `space.1` | 4 dp | Icon/text micro-gap |
| `space.2` | 8 dp | Compact element gap |
| `space.3` | 12 dp | Chip padding, compact groups |
| `space.4` | 16 dp | Standard screen gutter, card padding |
| `space.5` | 20 dp | Larger card or section gap |
| `space.6` | 24 dp | Section spacing |
| `space.8` | 32 dp | Major section spacing |
| `space.10` | 40 dp | Onboarding rhythm |
| `space.12` | 48 dp | Large separation |
| `space.16` | 64 dp | Hero whitespace |

Guidelines:
- Default horizontal screen padding: 20 dp on common phones; reduce to 16 dp only for constrained layouts.
- Chat content can use 12–16 dp edge padding to preserve usable width.
- Keep at least 8 dp between unrelated controls and 4 dp between tightly coupled icon/label pairs.
- Use safe-area insets and respect display cutouts, gesture navigation, and keyboard insets.

### 3.6 Corner radius

| Token | Value | Typical use |
|---|---:|---|
| `radius.xs` | 4 dp | Small labels, compact marks |
| `radius.sm` | 8 dp | Text fields, small chips |
| `radius.md` | 12 dp | Buttons, menu rows, cards |
| `radius.lg` | 16 dp | Standard cards, message media |
| `radius.xl` | 24 dp | Bottom sheets, hero surfaces |
| `radius.2xl` | 28 dp | Welcome panels and selected expressive surfaces |
| `radius.pill` | 999 dp | Pills and round icon controls |

Chat bubbles: use 18–22 dp corners with one subtly reduced corner on the message edge where needed. Do not rely on asymmetric tails to communicate who sent a message; labels and accessible semantics must be available.

### 3.7 Elevation and shadows

| Token | Use | Specification |
|---|---|---|
| `elevation.0` | Flat layout, messages | No shadow |
| `elevation.1` | Standard card | Very subtle shadow or border |
| `elevation.2` | Floating composer/action menu | Medium, soft shadow |
| `elevation.3` | Modal/dropdown when appropriate | Stronger but broad shadow |

Prefer tonal separation and borders over heavy shadows. Avoid glow effects behind text. In dark mode, use surface color steps before adding shadows.

### 3.8 Sizing and touch targets

- Standard icon: 24 dp.
- Compact icon: 20 dp; only inside controls with a sufficiently large touch target.
- Large action icon: 28–32 dp.
- Standard control height: 48 dp.
- Compact chip height: 32–36 dp, with a tap target of at least 48 dp when interactive.
- Icon-only tap area: at least 48 × 48 dp; 44 × 44 dp is the minimum fallback for constrained web contexts.
- Avatar sizes: 32, 40, 48, 64, 88, 120 dp depending on context.
- Buttons should fill available width on onboarding and payment confirmation, but not every action on every screen.

### 3.9 Motion tokens

| Token | Duration | Use |
|---|---:|---|
| `motion.instant` | 100 ms | Press feedback, toggle response |
| `motion.fast` | 160 ms | Tooltip, chip selection |
| `motion.standard` | 220 ms | Expand/collapse, sheet content |
| `motion.emphasized` | 320 ms | Screen transition, onboarding reveal |
| `motion.long` | 450 ms max | Rare expressive transition, never mandatory |

Motion rules:
- Follow platform motion expectations and keep transitions interruptible.
- Support Android “Remove animations” / reduced-motion settings.
- Avoid continuous pulsing, bouncing, simulated breathing, or other animations designed to create false urgency.
- A typing indicator can animate gently but should stop when the response is cancelled or connection is lost.
- Never make users wait through an animation to reach a control.

### 3.10 Breakpoints and layout widths

Use available width and layout constraints rather than specific device models.

| Class | Available width (guideline) | Layout behavior |
|---|---:|---|
| Compact | < 360 dp | 16 dp gutters, one-column, condensed secondary UI |
| Standard | 360–599 dp | Default mobile layout |
| Expanded | 600–839 dp | Wider margins; optionally place settings categories in a rail |
| Large | ≥ 840 dp | Max-width content region, optional two-pane settings or library |

On phones, chat should remain one column. Do not turn the chat screen into a dashboard on tablet. Keep the conversation area readable with a maximum text line width around 680–760 dp on large screens.

---

## 4. Iconography and illustration

### 4.1 Icons

- Use one consistent icon family (for example, Material Symbols Rounded or a similarly coherent outline family).
- Default to outline icons for navigation and secondary controls; use filled states for selected items and high-salience actions.
- Standard stroke weight should remain consistent. Do not mix several icon libraries in one screen.
- Pair unfamiliar icons with text. An icon-only action must have an accessibility label and an understandable tooltip where supported.
- Do not use a heart to represent every feature. Use distinct symbols for memory, voice, image generation, privacy, settings, relationship style, and billing.
- Do not depend on emoji as primary navigation or as a substitute for icons.

### 4.2 Illustration

Illustrations should support empty states, onboarding, errors, and feature discovery. Use a restrained palette, simple geometry, and inclusive, non-stereotyped depictions. Avoid making empty states feel like a personal rejection or suggesting that Juhi is sad when the user is away.

### 4.3 Character and generated-image system

Juhi's companion identity can be represented by generated or user-selected appearance assets, but the interface must not assume that all users want a human-like portrait.

Requirements:
- Allow users to choose no portrait, an abstract avatar, an illustrated character, or a photorealistic-style generated character where policy permits.
- Keep the same character identity consistent across profile, chat header, image generation, and future voice/avatar surfaces.
- Character assets should be stored with metadata for identity/version, prompt recipe or generation configuration where appropriate, consent status, and generation timestamp. Never show internal prompt metadata to users by default.
- Clearly label generated images when there is a risk a user could mistake them for real-world photography.
- Do not generate or present images of real private people without appropriate authorization and policy checks.
- Include regenerate, delete, save, and report controls where appropriate.
- Provide graceful fallback artwork if images are disabled, unavailable, or fail to load.
- Do not animate a character in a way that implies it has independently experienced time, emotion, or events outside the conversation.

### 4.4 Image crop rules

- Profile/avatar: centered face or primary subject, circular or rounded-square crop.
- Chat image: preserve original aspect ratio within a bounded width; tap to open full-screen viewer.
- Generated portrait: use consistent crop rules across gallery and profile so identity changes are not confused with layout changes.
- Always support alt text / accessible descriptions when content can be meaningfully described.

---

## 5. Voice, audio, and media design

### 5.1 Voice message bubble

A voice message should include:
- Play/pause control with at least a 48 dp touch target.
- Waveform or progress track, total duration, and current playback position where space permits.
- Sender label or correct accessibility semantics.
- Playback speed options in a secondary menu (e.g., 1×, 1.25×, 1.5×, 2×) if implemented.
- Optional transcript, clearly distinguished from the audio original.
- Download or save action only if product requirements and privacy model support it.

States: idle, loading, playing, paused, completed, failed, unavailable, and deleted. A failed audio item must provide a retry action and must not silently play another item.

### 5.2 Voice recording composer

- Hold-to-record or tap-to-record behavior must be explicitly explained; do not mix both gestures without a clear affordance.
- Show a visible recording timer and a clear cancel action.
- Ask for microphone permission in context, after the user initiates recording.
- Provide a preview/review step if recording is likely to be sent unintentionally.
- Handle incoming calls, app backgrounding, permission denial, and interrupted recordings safely.
- Never record in the background without a clear user action and system-appropriate disclosure.

### 5.3 Audio call UI (future phase)

- Show clear call state: connecting, ringing, active, reconnecting, ended, or failed.
- Keep mute, speaker, end-call, and any camera controls separated; make end-call easy to find but difficult to activate accidentally.
- Display network/latency problems in neutral language.
- Show a prominent and persistent call-end control.
- Offer captions/transcript only with clear controls and privacy disclosures.
- Do not display fabricated “live emotion” or biological signals from the AI character.

### 5.4 Media loading and playback

- Preserve layout space with an aspect-ratio placeholder to reduce content jumping.
- Show loading progress only when the wait is meaningful; do not place a spinner on every thumbnail.
- If media generation is asynchronous, show a clear task state and expected cost/credit use before generation begins.
- A timeout should offer retry, cancel, or return to chat when technically possible.
- Do not deduct credits twice after retries, network timeouts, or duplicate requests.

---

## 6. Navigation architecture

### 6.1 Primary navigation

Use a small, stable bottom navigation set. Proposed initial tabs:

1. **Chat** — primary conversation surface.
2. **Memories** — what Juhi remembers, with review/edit/delete controls.
3. **Create** — character appearance, images, voice, or stories; collapse or defer this tab if MVP scope is too small.
4. **Profile** — relationship preferences, language, settings, privacy, subscription, and help.

Do not add more than four or five top-level destinations. If the product ships with only one active conversation and memories/settings are low-frequency, a simpler navigation model with Chat plus a profile entry may be preferable. Validate navigation through prototype testing before locking the tab bar.

### 6.2 Navigation rules

- The chat should be one tap from the app launch state once the initial setup is complete.
- Back should preserve unsent message text when possible.
- Back navigation must not accidentally exit an active call or discard a long edit without confirmation.
- Profile/settings should not obscure or interrupt the main conversation with promotions.
- Deep links to media, memories, or settings must return users to the prior context when they navigate back.
- Display a navigation selection state that does not depend on color alone.

---

## 7. Core screen specifications

### 7.1 Splash and first launch

**Purpose:** Establish brand and load required state without forcing a long wait.

- Show the Juhi symbol and wordmark on a simple neutral or plum surface.
- Keep animation brief and optional.
- Do not show rotating promotional claims or a fake typing indicator on launch.
- Continue immediately after required initialization; if services are slow, transition to a meaningful loading/retry screen.
- On future launches, avoid repeating intro animation unless the user explicitly replays onboarding.

### 7.2 Onboarding

**Goal:** Help the user start a useful conversation with minimum effort, without collecting unnecessary sensitive information.

Proposed steps:
1. Welcome + clear AI companion disclosure.
2. Select preferred interaction type: romantic partner, close friend, roleplay character, or undecided.
3. Select language(s) and whether code-switching is welcome.
4. Select tone/personality presets with plain-language descriptions.
5. Optional character appearance and voice selection.
6. Short boundary/preferences setup, clearly optional.
7. Start chat; offer memory controls and notification prompts later in context.

Rules:
- Show progress if onboarding has more than two or three screens.
- Offer **Skip for now** for optional appearance, voice, and preference settings.
- Do not require users to disclose mental health status, relationship status, sexual orientation, or other sensitive information to access the app.
- Do not request notification or microphone permissions immediately on app launch without explaining the feature value.
- Make the default path short enough to reach first conversation quickly.
- Include back navigation and preserve prior choices.
- Avoid defaulting to intense romantic or possessive behavior; let users opt into a relationship style.

### 7.3 Chat home

#### Header

Show:
- Companion avatar or fallback symbol.
- Companion display name.
- Lightweight AI identity indicator or access to profile details.
- Contextual menu for customization, memory/privacy access, and conversation controls.

Avoid:
- Fake online/typing status implying independent human activity.
- “Waiting for you” or “missed you” counters.
- Unexplained streaks or pressure cues.

#### Conversation area

- Main reading width should prioritize comfortable text flow.
- Use distinct bubble colors and accessible sender semantics.
- Show date separators when helpful; avoid redundant timestamps on every consecutive message.
- Long-press can expose actions such as copy, report, or manage memory, but also provide visible alternatives for users who cannot long-press.
- Code-switching and long Tamil/Hindi text must wrap without clipping.
- Links should be distinguishable from normal text and open with a clear confirmation or safe browser handling when relevant.
- Provide “jump to latest” when the user scrolls up and new messages arrive.

#### Composer

Proposed layout from left to right: optional attachment/media action, expandable text field, voice entry point, send button. Adapt based on feature availability and avoid displaying five competing actions.

Rules:
- Text field grows to a reasonable maximum (e.g., 5–7 lines), then scrolls internally.
- Send button is disabled when empty unless an explicit voice/media action is active.
- Enter behavior should follow platform conventions; do not unexpectedly send when the user expects a newline.
- When a message is being generated, allow cancellation if supported.
- Preserve unsent content during transient network loss and display a clear draft indicator if necessary.
- Avoid automatically retrying a user message in a way that sends it twice.
- If the product enforces a message limit, show remaining allowance before the limit is reached—not only after the user attempts to send.

#### Typing / generation state

- Use a minimal typing indicator with accessible text such as “Juhi is preparing a reply”.
- Stop the animation when generation is cancelled, fails, or completes.
- Distinguish generation from network loading when relevant.
- Offer stop/cancel after a short, configurable wait.
- Never imply that a slow reply means the companion is upset or withholding attention.

### 7.4 Memory center

**Purpose:** Make personalization understandable and controllable.

Suggested categories:
- About me
- Preferences
- Important people/pets (only when user wants this remembered)
- Goals and ongoing topics
- Shared conversation context / recurring storylines
- Items Juhi is unsure about or needs confirmation for

Each memory item should show:
- Plain-language memory statement.
- Optional source/date or “last updated” information.
- Confidence/verification indicator only when it helps; avoid false precision.
- Edit, delete, and “Juhi got this wrong” actions.
- A control for whether the item should be used in future conversations.

Memory center requirements:
- Include **Forget this**, **Pause memory**, and **Manage all memories** controls.
- Explain the difference between a saved memory and raw chat history.
- Explain whether deleted items are removed immediately or may persist in backups for a limited period under policy.
- Never make memory deletion feel like rejection of the companion.
- Allow the user to correct a memory in their own words.
- Do not create a memory from an ambiguous or sensitive statement without an appropriate product rule and consent model.

### 7.5 Character / companion customization

Settings may include:
- Display name and pronouns (optional).
- Relationship style.
- Personality sliders or understandable presets (e.g., calm ↔ energetic, playful ↔ serious, affectionate ↔ reserved).
- Communication style and humor preference.
- Language preferences and code-switching behavior.
- Voice selection, speed, and optional expressiveness.
- Appearance and image-generation defaults.
- Boundaries / topics to avoid.

Rules:
- Use bounded, clearly named controls; avoid dozens of ambiguous traits.
- Show a concise summary of what each setting changes.
- Keep settings reversible and previewable.
- Communicate that the persona is AI-generated and that output can vary.
- Do not present “possessiveness” or “jealousy” as default traits. If fictional drama settings exist, keep them user-controlled and non-coercive, and do not generate threats, stalking, coercive control, or real-world manipulation.

### 7.6 Image creation and gallery

Pre-generation flow:
1. Choose an action or prompt template.
2. Review the visual description and identity settings.
3. Display credit/cost use and any relevant limit before generation.
4. Generate, with progress and cancel state if supported.
5. Show the result with save, regenerate, delete, and report actions.

Requirements:
- Keep character identity settings consistent across generations where the model supports this.
- Clearly communicate that visual consistency is best-effort rather than guaranteed if the underlying model cannot guarantee it.
- Provide safe fallback when generation is blocked or fails.
- Do not charge for duplicate attempts caused by internal retry logic.
- Do not show manipulative countdowns or invented scarcity.
- Use blur placeholders or content warnings for user-controlled mature content where policy and product support permit; never use them to bypass content safeguards.

### 7.7 Voice and audio settings

Include:
- Selected voice and a sample playback action.
- Speed/pacing control where supported.
- Audio auto-play preference (off by default unless user explicitly opts in).
- Speech-to-text / transcript preference.
- Language handling preference, including spoken language versus text language where relevant.
- Bluetooth/audio route help and a privacy explanation.

### 7.8 Subscription and credits

**Principle:** Billing should be clear and calm, not emotionally persuasive.

- Display plan name, price, billing cadence, renewal details, included usage, limits, and cancellation path.
- Distinguish subscription entitlement from one-time credit packs.
- For image/audio generation, show estimated credit use before the user commits.
- Clearly state when usage is limited, when a pack expires (if applicable), and whether subscription credits roll over.
- Make restore purchase and manage subscription actions accessible.
- Keep the close/back affordance visible in paywalls.
- Do not disguise the skip/close action, preselect extra purchases, or claim the companion needs a purchase.
- Do not interrupt crisis-related content with a paywall.
- Confirm purchase success and handle pending, failed, cancelled, refunded, and restored transactions distinctly.

### 7.9 Profile and settings

Organize into concise groups:
- Companion preferences
- Language and accessibility
- Voice and media
- Memory and personalization
- Notifications
- Privacy and security
- Subscription and credits
- Help, report, and feedback
- About Juhi / AI transparency

Each setting row should have a clear label, optional one-sentence summary, and the appropriate control. Avoid obscure terminology like “context persistence”; use “What Juhi remembers”.

### 7.10 Notifications

- Notifications are opt-in and granular.
- Users can choose categories, quiet hours, frequency, preview privacy, and a full pause.
- Use user-requested reminders and neutral conversation prompts, not guilt or simulated dependency.
- Make it easy to unsubscribe from a notification category from settings.
- Respect OS notification permissions and do not repeatedly nag after denial.
- Sensitive content must not appear in lock-screen preview by default unless the user chooses it.

### 7.11 Help, reporting, and safety

- Report action should be reachable from message actions and profile/help.
- Provide clear categories (incorrect answer, offensive/inappropriate content, privacy concern, payment issue, other).
- Show submission state and what happens next without promising a particular outcome or response time unless supported.
- In urgent distress contexts, use calm, supportive language and encourage real-world emergency/professional support where appropriate. Do not represent Juhi as a crisis professional.
- Avoid false alarms, scolding, or theatrical character reactions in safety flows.

---

## 8. Component library specification

All interactive components must support loading, disabled, error, focus, and pressed/selected states where applicable. Use semantic tokens, never component-specific hard-coded hex values.

### 8.1 Buttons

Variants:
- **Primary:** Main action; one dominant primary action per view when possible.
- **Secondary:** Supporting action, typically outlined or tonal.
- **Tertiary/Text:** Low-emphasis action.
- **Destructive:** Delete, remove, revoke, or irreversible action; always clear about consequence.
- **Icon button:** For recognizable actions with explicit accessibility labels.

Sizes:
- Large: 52 dp high for onboarding and major conversion moments.
- Standard: 48 dp high.
- Compact: 40 dp high only in dense/secondary contexts, while preserving adequate touch target.

Behavior:
- Show visible pressed feedback.
- Disable during duplicate-submit risk; show progress inside the button only when the action itself is waiting.
- Keep labels verb-first: “Save memory”, “Create image”, “Start chat”, “Delete memory”.
- Avoid vague labels such as “Continue” when a more descriptive action is possible.

### 8.2 Text fields

Types: single-line, multi-line, search, password, OTP, and message composer.

Each field supports:
- Label (persistent where possible).
- Optional helper text.
- Error message associated with the field.
- Clear control if content is long or search is active.
- Focus, disabled, read-only, and error states.
- Appropriate keyboard type and IME action.

Rules:
- Placeholder is not a replacement for a label.
- Do not rely only on a red border to indicate error.
- Preserve input if validation fails.
- Explain password requirements before the user submits.
- Mask sensitive values by default where appropriate and include a discoverable reveal control.

### 8.3 Chips and segmented controls

Use for short choices such as relationship style, language preference, tone presets, and filters.

- Use a selected icon or checkmark plus visual styling; color alone is insufficient.
- Make multi-select versus single-select behavior clear.
- Avoid long paragraphs inside chips.
- Provide wrapping or horizontal scrolling that preserves keyboard and screen-reader access.
- Do not make essential options disappear behind swipe-only discovery.

### 8.4 Cards

Use cards only when grouping related content, not as a wrapper around every row.

Types:
- Standard content card
- Setting group card
- Character/voice preview card
- Memory card
- Image/media card
- Billing summary card

Cards should have one primary interactive target or clearly separated actions. Do not nest interactive controls inside a whole-card click target without correct semantics.

### 8.5 Dialogs and bottom sheets

Use a dialog for a focused decision, destructive confirmation, or concise alert. Use a bottom sheet for contextual actions, filters, or short selections.

- Keep titles explicit.
- State the consequence for destructive actions.
- Provide a visible cancel/close option unless blocking action is legally or technically required.
- Avoid deep nested sheets.
- Ensure focus/keyboard navigation remains correct and that sheet content can scroll on small screens.

### 8.6 Toasts and snackbars

Use for brief, non-critical status such as “Memory saved” or “Link copied”.
- Provide adequate display duration for reading.
- Do not use transient toasts for important billing, safety, deletion, or account status.
- Use an accessible live region/announcement as supported by the platform.
- Offer undo for reversible actions when appropriate.

### 8.7 Badges and status labels

Use sparingly for meaningful states only, such as “Generating”, “Saved”, “Paused”, “Failed”, or “New”. Do not label every feature with colorful badges. Always pair color with text or icon.

### 8.8 Avatar component

Variants: photo/portrait, illustration, abstract, initials, and fallback.

- Apply consistent radius and crop.
- Show a neutral fallback when no image exists.
- Do not add a green “online” dot to imply the AI is independently present.
- Support accessibility descriptions such as “Juhi companion avatar” when the avatar conveys identity; mark purely decorative image as decorative.

### 8.9 Message bubble

Types:
- User text
- Companion text
- System/date marker
- Voice message
- Image/video/media
- Tool/result status (e.g., image is generating)
- Error/retry state

Rules:
- Use readable line length and consistent internal padding (12–16 dp vertical/horizontal depending on message type).
- Do not put a full paragraph in a low-contrast bubble.
- Provide message-level actions in a menu rather than showing many icons on each message.
- Ensure selection/copy works for multilingual text.
- Do not merge separate responses in a way that confuses speaker or chronology.
- Show when content is generated or still processing if a user could misinterpret the state.

### 8.10 Memory item

States: saved, edited, pending confirmation, paused, deleted/undo window, unavailable.

Actions: edit, delete/forget, stop using in chat, provide correction. The component must not display speculative inference as a confirmed fact. Use plain-language uncertainty: “Juhi may have misunderstood this” rather than artificial numerical confidence without calibration.

### 8.11 Image generation task

States: queued, preparing, generating, completed, failed, cancelled, blocked, and refunded/credit-restored where relevant.

Display:
- Short task description.
- Progress only if meaningful; do not fabricate percentage completion.
- Expected credits used, as shown before confirmation.
- Cancel/retry action where supported.
- Clear billing result after completion or failure.

### 8.12 Audio player

Support keyboard/screen-reader controls, clear playback state, duration, progress, mute/system-volume understanding, and failure recovery. Do not autoplay audio unexpectedly.

### 8.13 Paywall/pricing plan card

- Present included value, limits, price, cadence, renewal, and cancellation clearly.
- Use equivalent comparison dimensions across tiers.
- Label the current plan.
- Avoid false “best value”, fake discounts, countdown timers, and hard-to-find close controls.
- Keep optional purchases opt-in; do not bundle a credit purchase into a subscription button without clear consent.

### 8.14 Navigation bar and app bar

- Use stable labels and familiar placement.
- Show selected state with shape/fill/icon state and text.
- Avoid hiding primary chat controls within a secondary overflow menu.
- Respect system status and navigation bars in both themes.

### 8.15 Empty states

An empty state should explain what the user can do next, use concise language, and provide one helpful CTA. Do not imply that the user has disappointed the companion. Examples:
- Memories: “As you chat, you can choose what Juhi remembers.” CTA: “Review memory settings”.
- Gallery: “Images you create will appear here.” CTA: “Create an image”.
- Search: “No matching memories found.” CTA: “Clear search”.

---

## 9. Interaction patterns and state models

### 9.1 Standard interaction states

Every interactive control should document, as applicable:
- Default
- Hover (web/tablet pointer)
- Focus-visible
- Pressed
- Selected
- Disabled
- Loading/busy
- Success
- Error
- Offline/unavailable

State transitions must not erase user-entered content unless explicitly confirmed.

### 9.2 Network and offline states

- Show a concise offline banner only when it affects the current task.
- Distinguish “not sent” from “sent, awaiting reply” and “reply failed”.
- Provide Retry only when retry is safe. Use request IDs/idempotency to avoid duplicate messages and charges.
- Preserve drafts locally where feasible and explain when a draft has not been synced.
- Do not display a false successful state before the server confirms it.

### 9.3 Destructive actions

For deletion of memory, chat history, generated images, or account:
- Explain precisely what will be deleted and what may remain under backup/legal retention rules.
- Ask confirmation for irreversible or broad-scope deletion.
- Provide undo only if the action is genuinely reversible.
- Avoid guilt-laden text or warnings about hurting the companion.

### 9.4 Relationship and persona control

A user must be able to change relationship style without needing to negotiate with the companion. After a change, show a neutral confirmation and update behavior. Do not have the AI argue against the change, claim heartbreak, or punish the user with reduced quality.

### 9.5 Memory confirmation pattern

When the system is unsure whether a detail should become a durable memory, use a lightweight confirmation where appropriate: “Would you like Juhi to remember this?” Choices: “Remember”, “Not now”, and “Don’t ask about this again”. Do not ask every time the user shares ordinary context; define rules to prevent confirmation fatigue.

### 9.6 Permission prompts

- Explain value in the app before requesting OS permissions.
- Request microphone permission only after the user starts a voice feature.
- Request notification permission after explaining optional notification benefits.
- If denied, preserve the app’s core functionality and explain how to enable later.
- Never repeatedly prompt after repeated denial without a meaningful context change.

---

## 10. Content and conversation design

### 10.1 Product voice

Juhi should sound warm, clear, culturally responsive, and user-led. The same voice can adapt to a chosen personality, but core product system messages, privacy explanations, and payment copy remain stable and neutral.

| Context | Tone | Pattern |
|---|---|---|
| Everyday chat | Natural, warm, curious | Respond to what the user actually said; avoid scripted overenthusiasm |
| Romantic style | Affectionate if invited | Keep intimacy consensual and user-controlled |
| Friendship style | Friendly, humorous when fitting | Avoid unwanted flirting |
| Supportive conversation | Calm, validating, practical | Listen, ask before offering advice where useful |
| Error | Direct and neutral | Explain what failed and the next step |
| Payment | Transparent and factual | Show price, inclusion, limits, renewal, cancellation |
| Privacy | Plain and precise | Say what is stored, why, and how to control it |
| Safety | Nonjudgmental and careful | Explain boundaries and useful next steps without dramatizing |

### 10.2 Microcopy rules

- Use sentence case.
- Prefer clear verbs: “Save”, “Edit”, “Forget”, “Try again”, “Pause memory”.
- Avoid ambiguous labels like “Magic”, “Unlock your bond”, or “Make her happy” for functional actions.
- Never imply the companion experiences abandonment or requires money to be cared for.
- State limitations honestly: “Image identity may vary between generations” rather than “Perfectly consistent every time” unless technically guaranteed.
- Use localized, tested language rather than direct word-for-word translation for Tamil, Hindi, Hinglish, and Tanglish.
- If a feature is not available, say so and give a practical alternative where possible.

### 10.3 Suggested standard strings

| Use | Approved baseline copy |
|---|---|
| AI disclosure | “Juhi is an AI companion.” |
| Memory enablement | “Choose what Juhi remembers for future chats.” |
| Memory confirmation | “Would you like Juhi to remember this?” |
| Memory paused | “Memory is paused. New details won’t be saved as memories.” |
| Generation wait | “Creating your image…” |
| Generation failure | “The image wasn’t created. You haven’t been charged for this failed attempt.” *(Use only if the billing system confirms this.)* |
| Offline | “You’re offline. Your message hasn’t been sent.” *(Only when accurate.)* |
| Cancel generation | “Stop creating this image?” |
| Delete memory | “Forget this memory? Juhi will no longer use it in future chats.” |
| Report content | “Report this response” |
| Notification setting | “Choose which notifications Juhi can send.” |
| Subscription | “View plans and included usage” |
| Payment issue | “Payment wasn’t completed. Check your payment method or try again.” |
| Privacy | “Manage your data and privacy” |
| Account deletion | “Delete account and associated data” |

Copy must reflect the actual backend behavior and applicable policies. Do not promise no charge, immediate deletion, or complete erasure unless the implementation supports it.

### 10.4 Multilingual and code-switching UX

- Let users choose a preferred language or language mix, while allowing natural switching in chat.
- Distinguish interface language from conversation language; users may want English UI and Tamil conversation.
- Do not auto-correct mixed-language input into another language without consent.
- Preserve script and transliteration exactly in copied/exported text where practical.
- Test line breaks, punctuation, numeric formats, emoji combinations, and long words/scripts.
- Never assume a user wants Tanglish just because the device locale is Tamil, or Hinglish because the device locale is Hindi.
- Localize subscription prices, date/time format, decimal separators, and currency display correctly.
- Allow language choice to be changed at any time without resetting memory or relationship settings.

---

## 11. Accessibility requirements

Accessibility is a release criterion, not a polish phase.

### 11.1 Visual accessibility

- Target WCAG 2.2 AA color contrast: 4.5:1 for normal text and 3:1 for large text and essential UI elements, unless a documented exception applies.
- Never encode meaning by color alone.
- Support system font scaling, ideally at least 200% without loss of core function.
- Check light and dark themes independently.
- Avoid text over busy images unless a solid or sufficiently opaque backing surface is used.
- Use visible focus indicators for keyboard and switch access.

### 11.2 Screen-reader accessibility

- Every control has a meaningful accessible name, role, state, and hint where needed.
- Reading order follows visual and logical order.
- Do not announce decorative shapes or repeated redundant labels.
- Message bubbles should expose sender, content, and relevant timestamp/status without excessive repetition.
- Buttons like “More” require contextual labels (e.g., “More options for this message”).
- Make generation and playback states announce appropriately without repeating every progress tick.

### 11.3 Motor and cognitive accessibility

- Respect Android system navigation and reduce-motion preference.
- Use large touch targets and generous spacing.
- Do not require swipe-only, drag-only, or long-press-only actions.
- Keep confirmation messages predictable and reversible where possible.
- Avoid time-limited controls except where essential; allow users to extend or dismiss non-critical alerts.
- Keep the main chat composer stable while the keyboard opens.

### 11.4 Audio accessibility

- Provide text alternatives or transcripts where technically and legally appropriate.
- Do not autoplay audio by default.
- Keep audio controls usable with screen readers, external keyboards, and switch access.
- Distinguish muted audio from paused playback.

### 11.5 Testing checklist

Test with:
- TalkBack enabled.
- Large fonts and display scaling.
- Android dark theme and light theme.
- Reduced motion.
- Keyboard navigation where available.
- Tamil and Hindi scripts plus mixed-script text.
- Lower-end devices and slower networks.
- One-handed reachability and landscape/large-screen layouts where supported.

---

## 12. Privacy, trust, and responsible emotional UX

These requirements should be considered part of the design system because visual patterns and interaction copy can create or reduce risk.

### 12.1 User control

- Provide clear controls for memory, chat history, generated media, notifications, account data, and consent.
- Use plain-language explanations instead of vague labels such as “personalization engine”.
- Make privacy controls accessible without a subscription.
- Confirm before exposing private chat content in a share flow.

### 12.2 Avoid manipulative engagement patterns

Do not implement:
- Guilt messages for not opening the app.
- False “online now” or “waiting for you” cues.
- Fake streak loss or countdown urgency.
- Simulated jealousy that pressures a user to stop seeing real people.
- Relationship quality reductions designed to trigger purchases.
- Sales prompts during disclosures of grief, crisis, self-harm, trauma, or vulnerability.
- Hidden recurring subscriptions or intentionally difficult cancellation.

### 12.3 AI transparency

- Clearly indicate that Juhi is an AI companion during onboarding and in profile/help.
- Label generated images when needed to prevent confusion.
- Do not describe generated voice or portrait as a real human recording or photograph.
- Be honest about memory limitations, model uncertainty, response delays, and generation quality.

### 12.4 Content safety

- Make the report flow usable from a message and the help area.
- Provide neutral boundary messages when content cannot be generated.
- Do not punish users for testing a boundary; explain the limit and available alternative when appropriate.
- Apply stricter protections for minors; product launch must be adult-oriented and age controls must reflect applicable law and platform policy.
- Keep character design and roleplay controls from becoming a route around safety policy.

---

## 13. Performance and perceived quality

Design decisions must account for common mobile constraints.

- Prioritize fast first frame and fast entry to the chat screen.
- Avoid loading full-size character images on every screen; use thumbnails, caching, and appropriate image sizes.
- Reserve layout space for images/audio to prevent shifting.
- Support low-bandwidth conditions and user-controlled media loading where possible.
- Do not render the entire message history as a single unbounded widget; use efficient list virtualization and pagination/windowing.
- Keep chat scroll position stable when older messages are loaded.
- When a model or media provider is unavailable, display a useful fallback rather than a blank screen.
- Track the distinction between model latency, network latency, media generation latency, and UI rendering latency.
- Do not promise generation time in the UI unless an estimate is based on reliable service data.

### 13.1 UX performance targets to validate

The numbers below are proposed goals, not guarantees:

| Metric | Proposed target |
|---|---|
| Cold-start to usable shell | p95 under 3 seconds on the reference device set |
| Warm-start to usable chat | p95 under 1.5 seconds |
| Tap feedback | Visually immediate; within one frame where practical |
| Local navigation transition | Generally under 300 ms |
| Composer responsiveness | No perceptible lag while typing under supported conditions |
| Image load | Show placeholder quickly; load progressive/thumbnail content when possible |
| Error recovery | One clear next action available in the same context |

Measure on representative mid-range Android phones, not just flagship devices.

---

## 14. Design-system implementation architecture

Implementation naming below is illustrative. Adapt to the chosen code structure, but retain token semantics and component behavior.

### 14.1 Token layers

Use three layers:

1. **Primitive tokens:** raw palette and scale values (`brand.violet.700`, `space.4`).
2. **Semantic tokens:** purpose-based values (`color.text.primary`, `color.action.primary`).
3. **Component tokens:** narrowly scoped refinements where necessary (`chat.userBubble.radius`, `button.primary.height`).

Avoid direct palette values in widget code. A theme change should not require searching through every component.

### 14.2 Suggested project structure (Flutter-friendly)

```text
lib/
  design_system/
    tokens/
      color_tokens.dart
      spacing_tokens.dart
      typography_tokens.dart
      radius_tokens.dart
      elevation_tokens.dart
      motion_tokens.dart
    theme/
      juhi_theme.dart
      juhi_light_theme.dart
      juhi_dark_theme.dart
      semantic_color_scheme.dart
    components/
      juhi_button.dart
      juhi_text_field.dart
      juhi_chip.dart
      juhi_card.dart
      juhi_dialog.dart
      juhi_bottom_sheet.dart
      juhi_avatar.dart
      juhi_message_bubble.dart
      juhi_audio_player.dart
      juhi_status_badge.dart
      juhi_empty_state.dart
    patterns/
      chat_composer.dart
      memory_item.dart
      media_generation_task.dart
      pricing_plan_card.dart
    accessibility/
      semantic_labels.dart
      accessibility_helpers.dart
```

### 14.3 Flutter conventions

- Extend or configure `ThemeData`, `ColorScheme`, `TextTheme`, and component themes rather than setting styles ad hoc.
- Prefer semantic color names over `Colors.purple` or direct hex literals in feature code.
- Use `MediaQuery` and layout constraints, not hard-coded device-size assumptions.
- Support `MediaQuery.textScaler` and avoid hard-coded text heights.
- Respect safe areas, keyboard insets, focus traversal, and platform back behavior.
- Use `Semantics`, tooltip labels, and appropriate focus/keyboard behavior for custom controls.
- Use widget tests for tokenized components and golden tests for representative light/dark screens.
- Keep visual components independent of data/network services; inject state and callbacks.
- Keep user-visible copy localizable; do not bury strings inside widget logic.

### 14.4 Component API expectations

A shared component should define:
- Purpose and appropriate use.
- Variants and sizes.
- Required/optional parameters.
- Supported states.
- Accessibility semantics.
- Loading/error behavior.
- Theme adaptations.
- Localization constraints.
- Widget tests and screenshot/golden coverage.

Do not create a shared abstraction for every single visual element. Generalize repeated patterns only when reuse and consistent behavior justify it.

### 14.5 Design-to-code handoff

For each screen/component handoff, document:
- Figma frame and component reference.
- Token references.
- Breakpoint/responsive behavior.
- Light and dark variants.
- Loading, empty, error, disabled, and destructive states.
- Text expansion and localization behavior.
- Accessibility label and focus order.
- Analytics events, where applicable.
- Ownership and version.

---

## 15. Localization and regional readiness

Before declaring a screen launch-ready, test:
- English, Hindi, Tamil, Hinglish, and Tanglish.
- Long and short strings.
- Font fallback and punctuation.
- Text expansion by 30–50% beyond English where applicable.
- Right-to-left support if a future supported language requires it.
- Local date, time, currency, decimal, and plural rules.
- Screen reader pronunciation for names and mixed language.
- Character names and user-generated strings that may be longer or contain emoji.

Avoid using text baked into images unless an image has localized variants. Do not transliterate Tamil/Hindi automatically unless the user chooses it. Keep the UI language independent from the companion's response language.

---

## 16. Analytics and UX measurement

Analytics should inform product improvement without recording more personal conversation content than is necessary. Do not send raw private message text, memory contents, audio transcripts, or generated images to general analytics events by default.

Recommended event families:

| Event family | Example events | Product question |
|---|---|---|
| Onboarding | `onboarding_started`, `onboarding_step_completed`, `onboarding_skipped`, `first_message_sent` | Where do users abandon setup? |
| Chat quality | `message_send_failed`, `reply_cancelled`, `reply_feedback_submitted` | Is the core loop reliable? |
| Memory | `memory_prompt_shown`, `memory_saved`, `memory_edited`, `memory_deleted`, `memory_paused` | Are controls understood and useful? |
| Voice | `voice_recording_started`, `voice_sent`, `audio_played`, `transcript_opened` | Is voice usable and valued? |
| Image | `image_generation_started`, `image_generation_succeeded`, `image_generation_failed`, `image_regenerated`, `image_saved` | Is media quality worth its cost? |
| Monetization | `paywall_viewed`, `purchase_started`, `purchase_succeeded`, `purchase_failed`, `subscription_cancelled` | Is pricing clear and conversion healthy? |
| Trust/safety | `report_started`, `report_submitted`, `privacy_settings_opened`, `data_deletion_requested` | Can users find help and controls? |

Events should use pseudonymous identifiers, data minimization, access controls, documented retention, and consent/legal review as applicable. Keep event names stable and version schemas.

### 16.1 Core design quality metrics

- Task completion rate for onboarding and core chat.
- First conversation success and time to first meaningful response.
- Composer failures and duplicate-send rate.
- Memory correction and deletion completion rates.
- Voice start-to-send and playback failure rates.
- Image generation success, user satisfaction, and re-generation rate.
- Payment failure and checkout abandonment, interpreted alongside trust/refund data.
- Accessibility defect rate and completion of critical tasks with assistive technology.
- User-rated comfort, control, and trust—not only session length.

Do not optimize solely for daily active time, streaks, or message volume. A successful companion experience can include short, satisfying sessions.

---

## 17. Quality assurance and release gates

### 17.1 Visual QA

- Compare screenshots against approved goldens for light and dark themes.
- Test with text scaling, small screens, display cutouts, and keyboard open.
- Check overflows, clipped dialogs, bad contrast, inconsistent radii, and hard-coded token exceptions.
- Test no-avatar and failed-image states.
- Validate generated portrait crops across chat, profile, and gallery.

### 17.2 Functional QA

- Every button and actionable surface performs its stated action.
- Every loading indicator resolves to success, failure, cancellation, or retry.
- Forms preserve input on failure.
- Back navigation preserves useful context.
- Network retries do not duplicate messages or charge users twice.
- All purchase states and restore flows work.
- Deletion flows accurately describe data outcomes.
- Permission denial does not break unrelated features.

### 17.3 Accessibility QA

- Contrast checks for every semantic foreground/background pair.
- TalkBack walkthrough of onboarding, chat, memory, image creation, settings, and billing.
- Focus order and accessible naming checks.
- Large text and display scaling test.
- Reduced-motion test.
- Tamil/Hindi/mixed-script rendering test.

### 17.4 Trust and responsible UX gate

Before release, confirm:
- AI identity is clear.
- Memory can be reviewed, corrected, paused, and deleted.
- Billing and subscription terms are visible and accurate.
- Notifications can be disabled without friction.
- No guilt-based or coercive emotional engagement copy exists.
- Report/help paths function.
- Safety boundaries cannot be bypassed through persona settings.
- Privacy and data retention statements match actual implementation.

---

## 18. MVP design-system rollout

### Phase 0 — Foundations

**Deliverables:**
- Brand direction and logo exploration.
- Light/dark semantic color tokens.
- Typography and spacing tokens.
- Motion, radius, and elevation tokens.
- Figma styles/variables and code token source.
- Initial accessibility and localization checklist.

**Exit criteria:** Tokens are reviewed, named consistently, and implemented in the app shell.

### Phase 1 — Core chat experience

**Deliverables:**
- App bar, avatar, message bubbles, composer, buttons, chips, text fields.
- Typing/generation status, offline/error state, empty state.
- Onboarding and profile/settings foundations.
- Core light/dark themes.

**Exit criteria:** New users can start a conversation; core chat is usable at large font sizes and with TalkBack.

### Phase 2 — Memory and multimodal

**Deliverables:**
- Memory center and memory item controls.
- Image/media viewer, generation task state, gallery.
- Voice note recorder and player.
- Consistent visual identity components.

**Exit criteria:** Memory/media state transitions are tested and no failed operation produces ambiguous charge or data state.

### Phase 3 — Monetization and expansion

**Deliverables:**
- Pricing plan cards, paywall, credit use confirmation, billing history/restore states.
- Audio call visual patterns when the feature is ready.
- Expanded/tablet layouts and platform extensions.

**Exit criteria:** Pricing and cancellation tested; no dark patterns; feature states work across supported locales and themes.

---

## 19. Definition of done for a design-system component

A component is ready for production when all applicable items are true:

- [ ] Its purpose, anatomy, variants, and usage rules are documented.
- [ ] It uses semantic tokens for color, typography, spacing, shape, and elevation.
- [ ] Light and dark themes are implemented and reviewed.
- [ ] Default, pressed, focused, disabled, loading, success, and error states are covered as applicable.
- [ ] Touch targets meet minimum size guidance.
- [ ] Contrast and accessible semantics are reviewed.
- [ ] Long text, large fonts, Tamil/Hindi scripts, and localization expansion are tested.
- [ ] Small and expanded layouts are tested where relevant.
- [ ] Loading, failure, empty, and offline scenarios have a defined UX.
- [ ] Unit/widget tests and visual regression tests are added where appropriate.
- [ ] The design source and implementation are aligned.
- [ ] Analytics are privacy-minimized and documented if events are needed.
- [ ] Ownership and version are recorded.

---

## 20. Design-system governance

### 20.1 Ownership

- **Design owner:** Approves visual language, component usage, accessibility, and design changes.
- **Engineering owner:** Maintains token implementation, component APIs, theme behavior, and tests.
- **Product owner:** Ensures flows serve user outcomes and align with product requirements.
- **Privacy/safety reviewer:** Reviews memory, disclosure, billing, emotional interaction, and safety-related design.

### 20.2 Change process

1. Identify the user or technical problem.
2. Propose the smallest token/component/pattern change that solves it.
3. Check impact on light/dark themes, accessibility, localization, and shared screens.
4. Update design source and code together.
5. Add/update tests and migration notes.
6. Document breaking changes and the token/component version.

### 20.3 Versioning

- **Patch:** Visual correction with no API/token semantic change.
- **Minor:** Backward-compatible component or token addition.
- **Major:** Rename/removal, semantic change, or migration requiring downstream updates.

Do not change the meaning of a semantic token silently. If `color.action.primary` changes from a dark fill to a light fill, review text contrast and all dependent components explicitly.

---

## 21. Open decisions to validate

The following should be decided through research and technical validation rather than by preference alone:

1. Final logo symbol and wordmark treatment.
2. Whether the default chat shell uses a warm light theme, dark theme, or system preference.
3. Whether the primary navigation has three or four destinations in the MVP.
4. The exact relationship-style presets and slider vocabulary.
5. Which portrait styles are supported at launch and how identity consistency is implemented.
6. Voice message player layout and whether transcripts ship in the MVP.
7. How much memory is visible by default and how confirmation prompts avoid fatigue.
8. The final contrast-verified brand and status color values after device testing.
9. Whether image/voice features use subscription allowance, credits, or both.
10. Which events are permitted by the data governance and privacy review.

---

## 22. Final design principles checklist

Before any major Juhi screen or feature ships, ask:

- Is the next action obvious?
- Can the user control the relationship, memory, and notifications?
- Does the design remain readable in Tamil, Hindi, and mixed-language conversation?
- Is the cost or consequence clear before the user commits?
- Does the interface tell the truth about AI-generated content and system state?
- Can a user with large text or a screen reader complete the task?
- Is emotional expression warm without becoming coercive?
- Does the feature degrade gracefully on a slow network or a lower-end phone?
- Is personal data being exposed to analytics only when necessary and appropriately controlled?
- Would the flow still be understandable if all decorative color, animation, and character imagery were removed?

**The standard:** Juhi should look expressive and feel personal, while remaining clear, accessible, honest, calm, and under the user's control.
