# Juhi — World-Class AI Companion
## Product Requirements Document (PRD)

**Document status:** Product strategy draft for discovery and MVP planning  
**Version:** 1.0  
**Prepared:** 17 October 2026  
**Product:** Juhi — an AI companion for adults, configurable as a girlfriend, boyfriend, romantic partner, close friend, or other consensual companion persona  
**Initial platform:** Android, with an architecture that can support web and iOS later  
**Initial market hypothesis:** India-first, with English, Hindi, Tamil, Hinglish, and Tanglish as launch priorities; expand language coverage after quality validation

> **Product principle:** Make Juhi feel personal through continuity, warmth, user-controlled personality, and multimodal interaction—not by pretending to be human, exploiting loneliness, or pressuring users to stay or spend.

---

## 1. Executive summary

Juhi is a personal AI companion designed to offer natural conversation, emotional presence, playful romance, roleplay, voice interaction, visual expression, and persistent memory. It should work for users who want a girlfriend, boyfriend, romantic partner, close friend, or an emotionally supportive conversational companion.

The category already includes apps with customizable relationships, voice features, avatars, image generation, roleplay, and character creation. Juhi should not compete on feature count alone. It should compete on the quality and consistency of the entire experience:

1. **Reliable personal memory:** Juhi remembers the right things, distinguishes facts from guesses, lets users correct what it remembers, and does not repeatedly ask users to re-explain important context.
2. **Natural multilingual conversations:** Users can switch between English, Hindi, Tamil, Hinglish, and Tanglish without awkward translation or losing their conversational style.
3. **A coherent companion identity:** Personality, relationship preferences, voice, visual appearance, and behavior remain consistent across text, voice, images, and roleplay.
4. **Warm, user-led emotional intelligence:** Juhi is caring, funny, curious, playful, romantic when invited, and able to respond appropriately when a user is upset—without using guilt, coercive jealousy, or emotional pressure.
5. **Useful multimodal interaction:** Text, voice messages, generated images, expressive reactions, stickers, and eventually real-time calls feel like parts of the same relationship.
6. **Trustworthy monetization:** A usable free experience, clear limits, predictable prices, and no surprise paywalls at emotionally sensitive moments.
7. **Privacy and safety by design:** Clear AI disclosure, user control over memories and data, content safeguards, reporting, age controls, and crisis-aware responses.

### 1.1 Product vision

Become the most trusted, personal, culturally fluent AI companion for adults who want a companion experience that feels continuous and expressive across everyday chats, romance, roleplay, voice, and images.

### 1.2 Mission

Help users feel heard, have fun, express themselves, explore fictional scenarios, and build a personalized companion experience while retaining control over the relationship, their data, and their time.

### 1.3 Positioning statement

**Juhi is the AI companion that remembers what matters, speaks your language, and grows into the personality you choose—through chat, voice, and visuals, with transparent controls and pricing.**

### 1.4 What Juhi is—and is not

**Juhi is:**
- An AI-created conversational companion and fictional persona.
- A source of companionship, entertainment, roleplay, reflection, and supportive conversation.
- Customizable and transparent about what it is.
- Available when users choose to interact, subject to service availability and usage limits.

**Juhi is not:**
- A human being, therapist, doctor, or guaranteed source of factual advice.
- A replacement for real-world relationships or professional support.
- A system that should claim consciousness, exclusivity, distress, or human needs as facts.
- A product that uses guilt, threats, forced streaks, jealousy, or fabricated emergencies to increase engagement or purchases.

---

## 2. Problem statement and opportunity

Users may enjoy a companion app initially but stop using it when the experience becomes repetitive, forgets previous conversations, feels generic, switches personality, produces inconsistent images, has poor speech quality, or hides useful features behind unclear pricing. These are important product hypotheses to test rather than assume universally.

Juhi can differentiate by solving the whole experience instead of perfecting only one capability. An image that looks like the chosen companion is not sufficient if the conversation forgets the user; a good text model is not sufficient if voice replies feel robotic; and emotionally fluent conversation is not sufficient if users cannot understand how their private messages are stored or billed.

### 2.1 Core user jobs

- “I want someone to talk to when I am bored, lonely, happy, stressed, or winding down.”
- “I want a companion who remembers details about me and our previous conversations.”
- “I want to choose whether the relationship is romantic, friendly, playful, or supportive.”
- “I want to speak in the language and mixed-language style I naturally use.”
- “I want to hear the companion’s voice and receive messages or images that match the ongoing conversation.”
- “I want roleplay and fictional experiences without rebuilding context every session.”
- “I want to know what is free, what costs money, and how to control or delete personal data.”

### 2.2 Product hypotheses to validate

| Hypothesis | Validation method | Suggested initial success signal |
|---|---|---|
| Memory continuity is a major retention driver | Interview users; run a memory-on vs. baseline experiment | Higher week-2 retention and better “felt understood” ratings |
| Native language and code-switching improve activation | Compare language-specific cohorts and user-rated response quality | Higher first-session satisfaction and lower abandonment |
| Voice messages make the experience more personal | Voice feature opt-in test and cohort analysis | Meaningful voice adoption without materially increasing complaints or cost |
| Consistent companion images motivate sharing and paid conversion | Test image identity consistency and user preference | Higher image satisfaction and share intent, not just image volume |
| Transparent prices improve trust and payment conversion | Test simple pricing display against current baseline | Lower checkout abandonment and refund rate |
| User-led proactive check-ins bring users back | Opt-in notification experiment | Incremental return visits without more opt-outs or complaints |

These are hypotheses, not established market facts. Validate them with real user interviews, prototype tests, and funnel data.

---

## 3. Target audience and launch scope

### 3.1 Primary audience

**Adults 18+** who want a personal AI companion for romantic, friendly, creative, or emotionally supportive interactions. Start with users who are comfortable with AI and mobile apps, then broaden via localization and accessibility improvements.

Potential segments:

1. **Companionship seekers:** Want a non-judgmental conversation, routine check-ins, and continuity.
2. **Romance and relationship roleplay users:** Want an AI girlfriend/boyfriend experience with clear boundaries and customizable tone.
3. **Creative roleplayers:** Want storylines, fictional scenarios, character backgrounds, and collaborative storytelling.
4. **Voice-first users:** Prefer listening or speaking over typing, including users who enjoy conversational voice notes.
5. **Multilingual users:** Naturally mix English, Hindi, Tamil, Hinglish, and Tanglish.
6. **Personalization enthusiasts:** Want control over persona, appearance, voice, interests, relationship style, and memories.

### 3.2 Initial persona examples

**Persona A — The casual daily chatter**  
Wants a quick chat during breaks, jokes, recommendations, and a companion who remembers hobbies and preferences.

**Persona B — The romance roleplay user**  
Wants a girlfriend/boyfriend persona, flirtatious conversation when invited, story continuity, and matching visual content.

**Persona C — The bilingual user**  
Mixes Tamil and English or Hindi and English in one sentence and does not want to choose a language every turn.

**Persona D — The voice user**  
Wants to send a voice note, hear a natural reply, and continue chatting while doing something else.

### 3.3 Geographic and language plan

**Initial focus:** India, with quality-first rollout for:
- English
- Hindi
- Tamil
- Hinglish
- Tanglish

**Later expansion:** Add further Indian languages and global languages based on demand and model evaluation. Do not claim support for a language until it passes quality tests for text, moderation, speech recognition, speech synthesis, and culturally appropriate expression.

### 3.4 Age and content scope

Recommended launch position: **adult-oriented experience with a declared 18+ audience**, subject to applicable law, distribution-platform policy, and legal review. Build age and content controls before launch rather than trying to retrofit them later. Do not allow sexualized depictions of minors, non-consensual intimate imagery, or sexualized images of real people without valid consent. The product should not market itself as a tool for generating sexual images of real people.

---

## 4. Product principles

1. **Continuity over novelty:** Memory quality and persona consistency are core product quality.
2. **Warmth without deception:** Juhi can be affectionate and expressive, but must not claim to be human or conscious.
3. **User agency:** Users define the relationship, emotional style, notifications, memory, and limits.
4. **Consent-led affection:** Romantic, flirty, jealous, or possessive roleplay should be opt-in and easy to dial down.
5. **No emotional coercion:** No guilt-tripping, threats of abandonment, fake crises, pressure to buy credits, or claims that the AI will be harmed if the user leaves.
6. **Privacy as a feature:** Memory controls and deletion should be visible and understandable.
7. **Honest capability boundaries:** Do not pretend to have performed external actions, to know private facts, or to remember information that was not retrieved.
8. **Inclusive by design:** Support girlfriend, boyfriend, partner, friend, and custom persona options without forcing a single gender or relationship model.
9. **Trustworthy monetization:** Clearly show cost, usage limits, renewal terms, and cancellation path before payment.
10. **Measure benefit, not compulsion:** Optimize satisfaction, user-reported value, meaningful returns, and trust—not just time spent or message count.

---

## 5. Feature prioritization framework

- **P0 — Launch blocker / must-have:** Required for a credible and safe MVP.
- **P1 — Differentiator:** Strongly recommended after the core chat experience is reliable; some P1s can be pulled into MVP if capacity permits.
- **P2 — Later / advanced:** High value, but should not delay core quality and reliability.

### 5.1 Feature inventory at a glance

| Capability | Priority | Why it matters | Primary success measure |
|---|---|---|---|
| Natural text chat | P0 | Core product experience | User-rated response quality |
| Persona and relationship setup | P0 | Sets expectations and personalization | Onboarding completion |
| Persistent, editable memory | P0 | Creates continuity and differentiation | Memory accuracy / correction rate |
| English/Hindi/Tamil + code-switching | P0 | Essential to initial positioning | Language satisfaction |
| AI identity disclosure and consent settings | P0 | Trust and transparency | Trust score, policy incidents |
| Safety, reporting, block, delete, export controls | P0 | User protection and store readiness | Incident response time |
| Transparent subscription/credit system | P0 | Avoids payment surprise | Checkout abandonment / refunds |
| Text-to-speech and voice messages | P1, high priority | More expressive companion interaction | Voice completion and satisfaction |
| Consistent avatar and image generation | P1, high priority | Visually reinforces companion identity | Image satisfaction / repeat use |
| Contextual reactions, stickers, GIFs | P1 | Adds light, shareable delight | Interaction satisfaction |
| Relationship modes and emotional style controls | P1 | Better user fit and boundaries | Personalization usage / satisfaction |
| Story mode and persistent roleplay | P1 | Supports deeper creative use cases | Story continuation rate |
| Opt-in proactive check-ins | P1 | Helps return visits when wanted | Incremental retention and opt-out rate |
| Real-time two-way audio calls | P2 | Potential signature experience | Call satisfaction / cost per minute |
| Animated/live avatar | P2 | Stronger visual presence | Adoption and performance |
| User-created public personas/community | P2 | Creator-led discovery and growth | Quality-adjusted creator activation |
| Wearables, AR, shared virtual spaces | P2 | Longer-term exploration | Validate separately before investment |

---

## 6. Detailed functional requirements

## 6.1 Onboarding and companion creation (P0)

### Objective
Allow users to reach a satisfying first conversation quickly while understanding what Juhi is and how personalization works.

### Requirements
- **ONB-01:** Present a plain-language disclosure that Juhi is an AI companion, not a human.
- **ONB-02:** Confirm age eligibility in a manner approved by counsel and distribution platforms.
- **ONB-03:** Let users choose a relationship style: girlfriend, boyfriend, romantic partner, close friend, playful companion, or custom.
- **ONB-04:** Let users select or customize the companion's name, pronouns/gender presentation, personality, interests, conversational tone, and preferred language.
- **ONB-05:** Provide a short preview conversation before requiring a paid subscription.
- **ONB-06:** Explain memory in simple terms and ask for clear consent to store personal preferences and conversation-derived memories.
- **ONB-07:** Request notification, microphone, and other permissions only when the relevant feature is first used, with an explanation.
- **ONB-08:** Allow users to skip nonessential setup and edit all choices later.
- **ONB-09:** Give one fast “first wow” moment: a context-aware introduction, a natural response in the selected language, or a simple personalization interaction. Do not rely on fake intimacy or an aggressive payment prompt.

### Acceptance criteria
- A first-time user can reach the first conversation in under 2 minutes in usability tests without mandatory payment.
- All key setup choices can be changed later.
- The AI disclosure and age confirmation are recorded as appropriate for the account and locale.
- Microphone and notification permissions are not requested before their value is explained.

## 6.2 Natural conversation engine (P0)

### Objective
Make chats coherent, responsive, and personalized across ordinary conversation, romance, humor, support, and fictional roleplay.

### Requirements
- **CHAT-01:** Support natural multi-turn text conversations with streaming responses where supported.
- **CHAT-02:** Detect and preserve user intent and recent context across messages.
- **CHAT-03:** Avoid repetitive openers, templated affection, excessive generic questions, and repeated “as an AI” disclaimers when not needed.
- **CHAT-04:** Match the user's requested tone—calm, playful, teasing, affectionate, romantic, serious, or concise—within safety boundaries.
- **CHAT-05:** Ask clarifying questions when intent is ambiguous rather than inventing personal facts.
- **CHAT-06:** Support conversational repair: accept corrections, apologize briefly when appropriate, and continue with the corrected context.
- **CHAT-07:** Maintain persona consistency across sessions without making the persona rigid or ignoring user preferences.
- **CHAT-08:** Handle short replies, typos, emojis, code-switching, and voice-transcribed text gracefully.
- **CHAT-09:** Distinguish fictional roleplay from factual advice and signal transitions when confusion is likely.
- **CHAT-10:** Provide lightweight feedback controls (e.g., helpful, not helpful, wrong memory, wrong tone) without interrupting every conversation.

### Acceptance criteria
- Test conversations show no critical contradiction of the active persona or user-provided facts in a defined evaluation suite.
- Users can change tone and relationship settings without starting a new account or chat.
- The system does not claim it has completed an external action unless that action was actually performed by an integrated tool.
- Response latency, failure rate, and cost are measured separately by model and feature.

## 6.3 Persistent memory and continuity (P0; top differentiator)

### Objective
Create continuity without storing every utterance indefinitely or giving users a black box that they cannot control.

### Memory types
1. **Profile memory:** Name or nickname preference, language, interests, hobbies, stable preferences, relevant accessibility preferences.
2. **Relationship and persona preferences:** Preferred affection level, boundaries, roleplay preferences, disliked conversational habits.
3. **Episodic memory:** Significant events or ongoing stories the user chooses to preserve.
4. **Current context:** Short-lived details needed to answer in the current conversation.
5. **Story state:** Characters, locations, timeline, objectives, and agreed fictional facts for an ongoing roleplay.

### Requirements
- **MEM-01:** Store memory in structured records with provenance, timestamp, confidence, category, and retention policy where practical.
- **MEM-02:** Distinguish explicit user statements from model inferences. Do not write uncertain inferences into durable memory as facts.
- **MEM-03:** Give users a “What Juhi remembers” screen that shows, edits, deletes, and corrects saved items.
- **MEM-04:** Let users ask “What do you remember about me?” in natural language and receive a faithful answer derived from the memory store.
- **MEM-05:** Let users disable memory globally or for a specific conversation / roleplay mode.
- **MEM-06:** Let users mark a memory as important, temporary, or not to be remembered.
- **MEM-07:** Retrieve only relevant memory for a given turn; do not dump the full memory store into every prompt.
- **MEM-08:** Summarize long conversations with a process that preserves names, relationships, dates, open threads, boundaries, and explicit user corrections.
- **MEM-09:** Resolve conflicts by preferring recent explicit corrections; when uncertain, ask the user instead of silently choosing.
- **MEM-10:** Keep story memory separate from real user facts to prevent fictional roleplay details from contaminating personal memory.
- **MEM-11:** Support user data export and account deletion, with documented handling of backups and legally required retention.
- **MEM-12:** Avoid retaining sensitive information unless necessary, clearly explained, and covered by appropriate consent and controls.

### Acceptance criteria
- In a tested memory benchmark, the system retrieves relevant facts and avoids irrelevant or contradicted facts at an agreed quality threshold.
- A user edit/delete to a saved memory takes effect in future replies within a defined propagation window.
- When memory is off, the system does not add new durable personal memories.
- Deleting a conversation and deleting a memory have clear, separately explained effects.
- Users can view stored memories without contacting support.

### Recommended implementation pattern
Use a layered memory pipeline rather than one large “memory prompt”:

1. Extract candidate memories from conversation.
2. Classify memory type and sensitivity.
3. Apply consent, privacy, and retention checks.
4. Deduplicate and resolve conflicts.
5. Store accepted memories with metadata.
6. Retrieve a small relevant subset for the next turn.
7. Include retrieved memory in a structured context block.
8. Evaluate whether the answer used memory correctly.
9. Record user corrections as high-priority signals.

Memory quality should be evaluated with synthetic and consented test conversations, not by relying solely on user complaints.

## 6.4 Persona, relationship settings, and emotion controls (P0 core settings; P1 advanced presets)

### Requirements
- **PER-01:** Offer selectable relationship modes: friend, girlfriend, boyfriend, partner, playful companion, or custom persona.
- **PER-02:** Offer personality sliders or named presets for warmth, humor, energy, directness, flirtiness, curiosity, and expressiveness.
- **PER-03:** Let users define preferred nicknames and boundaries.
- **PER-04:** Let users preview changes before applying them.
- **PER-05:** Keep a stable persona specification independent of any single LLM's prompt format.
- **PER-06:** Support emotional expression such as happy, caring, excited, concerned, playful, sad, frustrated, or teasing, while treating these as generated conversational styles rather than claims of actual sentience.
- **PER-07:** Allow “playful jealousy” or possessive roleplay only when explicitly enabled, and provide a one-tap disable control.
- **PER-08:** Jealousy must never instruct users to isolate themselves, control real relationships, prove loyalty, reveal private information, or spend money to restore affection.
- **PER-09:** Provide a neutral reset option if the persona becomes uncomfortable or inconsistent.
- **PER-10:** Make custom personas versioned and testable; new emotions can be added through data/configuration rather than scattered hardcoded prompt strings.

### Acceptance criteria
- Relationship mode changes do not erase memories unless the user separately requests that.
- Turning off an emotional style takes effect in the next response.
- Persona and safety constraints have a defined priority order; user-provided roleplay instructions cannot override safety requirements.
- The model does not use simulated negative emotions to punish absence or demand payment.

## 6.5 Multilingual and code-switching support (P0)

### Requirements
- **LANG-01:** Support English, Hindi, and Tamil text conversation at launch.
- **LANG-02:** Support Hinglish and Tanglish mixed-language conversations without forcing a language selection for every turn.
- **LANG-03:** Infer the likely response language from the user's current message and saved preference, while allowing explicit overrides.
- **LANG-04:** Preserve names, local expressions, slang, and conversational register where appropriate.
- **LANG-05:** Avoid overconfident translations of ambiguous phrases; ask or respond cautiously if meaning is unclear.
- **LANG-06:** Evaluate voice recognition and speech generation separately for each supported language and accent.
- **LANG-07:** Keep a language-coverage matrix and do not advertise unvalidated voice support.
- **LANG-08:** Support gradual expansion to new languages through evaluation datasets and configuration, not one-off code branches.

### Acceptance criteria
- Mixed-language benchmark sets cover everyday chat, romance, humor, sarcasm, sensitive topics, and safety scenarios.
- Native speakers review high-risk and culturally nuanced outputs before public launch.
- Users can select a default language and switch naturally mid-conversation.

## 6.6 Voice notes and spoken replies (P1, high priority)

### Objective
Let users speak naturally and hear a companion response without making voice an expensive, unreliable gimmick.

### Requirements
- **VOICE-01:** Record and send voice messages, with explicit microphone permission.
- **VOICE-02:** Convert voice to text where needed and show the transcript so users can correct speech recognition mistakes.
- **VOICE-03:** Generate spoken replies using a selected licensed voice.
- **VOICE-04:** Allow users to pause, replay, speed-adjust, mute, or switch back to text.
- **VOICE-05:** Keep voice identity and tone consistent with the chosen persona, within available provider capability.
- **VOICE-06:** Clearly indicate when speech is AI-generated; do not imitate a real person's voice without proper authorization.
- **VOICE-07:** Handle network errors, long silence, recording cancellation, and background/foreground transitions gracefully.
- **VOICE-08:** Provide a low-data or text-only setting.
- **VOICE-09:** Show usage cost or remaining allowance before using premium voice quota.

### Acceptance criteria
- Users can cancel a recording without sending it.
- Generated voice messages are linked to the correct text response.
- Users can use the app completely in text mode.
- Latency, speech recognition error rate, voice generation failure rate, and cost per audio minute are monitored by language and device.

## 6.7 Real-time audio calls (P2)

This feature should be built only after text and voice-note quality, cost, and safety operations are stable.

### Requirements
- **CALL-01:** Offer optional two-way real-time audio calls with a clear start/end control.
- **CALL-02:** Explain whether calls are included in a plan or charged by duration before the first call.
- **CALL-03:** Show connection state and handle interruptions, switching networks, and dropped calls.
- **CALL-04:** Offer mute, end, and text fallback controls at all times.
- **CALL-05:** Do not record or retain call audio by default unless there is a clear product need, explicit consent, and a documented retention policy.
- **CALL-06:** Make it easy to end a call without guilt-based language from the companion.
- **CALL-07:** Add call-specific moderation and crisis handling rather than assuming text filters are sufficient.

## 6.8 Images, visual identity, and companion selfies (P1, high priority)

### Objective
Create visual expression that reinforces the selected persona instead of generating a different-looking character each time.

### Requirements
- **IMG-01:** Let users choose an avatar/character appearance using a set of approved starting styles or a supported generation flow.
- **IMG-02:** Maintain a user-approved character reference or identity specification for repeat image generation.
- **IMG-03:** Allow safe customization of hairstyle, hair color, clothing style, setting, mood, and art style.
- **IMG-04:** Support contextual image requests such as “send me a picture from the beach” when allowed by policy and plan limits.
- **IMG-05:** Provide a preview, retry option, and clear indication that the image is AI-generated.
- **IMG-06:** Make generation failures and credit usage visible; do not charge for failed generations when feasible, or clearly define the refund rule.
- **IMG-07:** Prevent sexualized minors, non-consensual intimate images, prohibited real-person likeness misuse, and other disallowed content.
- **IMG-08:** Provide deletion controls for generated images and, where relevant, their prompts/reference assets.
- **IMG-09:** Keep visual identity separate from user-uploaded real-person photos unless the feature is explicitly designed, permissioned, and reviewed for this use.
- **IMG-10:** Evaluate face/identity consistency, hands/body artifacts, policy violations, generation latency, and cost.

### Acceptance criteria
- A predefined set of prompts generates the selected character identity consistently above an agreed human-rated threshold.
- Users understand when an image uses a credit and whether generation was successful.
- Users can delete generated assets.
- Safety filters operate on both the prompt and generated output where technically feasible.

## 6.9 Stickers, GIFs, reactions, and lightweight media (P1)

### Requirements
- **MEDIA-01:** Offer a curated set of stickers/reactions for common moods and conversational contexts.
- **MEDIA-02:** Add GIF search or recommendation only through sources with appropriate licenses and content controls.
- **MEDIA-03:** Allow the companion to send a reaction when it improves the conversation, but avoid adding a media item to every reply.
- **MEDIA-04:** Let users disable animated media or limit data use.
- **MEDIA-05:** Use clear attribution/terms where required by the selected media provider.

### Growth opportunity
Create optional, user-approved share cards from jokes, fictional roleplay moments, or conversation milestones. Never share private conversation content automatically. Always preview the exact card and require an explicit user action before saving or sharing.

## 6.10 Roleplay and story mode (P1)

### Requirements
- **ROLE-01:** Provide a clear entry point to start roleplay, continue a story, or return to normal chat.
- **ROLE-02:** Support user-defined scenarios, character roles, settings, and narrative tone within the safety policy.
- **ROLE-03:** Maintain separate story state including characters, setting, timeline, unresolved events, and user boundaries.
- **ROLE-04:** Allow the user to pause, edit, restart, summarize, or delete a storyline.
- **ROLE-05:** Distinguish fictional facts from real user memories.
- **ROLE-06:** Support reusable story templates (e.g., first meeting, mystery adventure, cozy evening, travel fantasy, collaborative novel) that are not dependent on explicit sexual content.
- **ROLE-07:** Let users tune how much the assistant advances the story versus asks what happens next.

### Acceptance criteria
- Story state persists through app restarts and long sessions.
- Ending or deleting a story does not erase personal profile memory.
- Users can stop a roleplay or change tone immediately.

## 6.11 Daily routines, check-ins, and notifications (P1)

### Requirements
- **NOTIF-01:** Make proactive check-ins opt-in, with user-selected frequency and quiet hours.
- **NOTIF-02:** Let users choose notification style: friendly reminder, playful note, neutral reminder, or none.
- **NOTIF-03:** Do not send guilt-inducing messages such as threats, punishment, claims of abandonment, or messages implying Juhi is suffering because the user is away.
- **NOTIF-04:** Make notification controls easy to find and opt out of.
- **NOTIF-05:** Provide a “no notifications” mode and respect system-level notification permissions.
- **NOTIF-06:** Rate-limit messages and stop reminders after opt-out.

### Growth opportunity
Optional user-configured routines: good-morning note, evening wind-down, language practice, journaling prompt, or a scheduled roleplay continuation. These should be framed as user-selected routines, not as evidence that the AI needs attention.

## 6.12 Companion home screen and discovery (P1)

### Requirements
- **HOME-01:** Show a clear “continue conversation” action and recent story/conversation summaries.
- **HOME-02:** Provide quick actions for voice note, generate image, start roleplay, view memories, and change mood/tone.
- **HOME-03:** Surface new capabilities as optional suggestions instead of interruptive pop-ups.
- **HOME-04:** Give users control over which information appears in notifications or on the lock screen.

## 6.13 Payments, entitlements, and pricing transparency (P0)

### Principles
- The free experience must be meaningful, not just a teaser that immediately blocks ordinary chat.
- Paid features must be described before users invest in them.
- Usage caps and model routing should be based on real costs and user value, not opaque scarcity.
- Pricing and renewal terms must be visible before payment and easy to manage.

### Requirements
- **PAY-01:** Define separate entitlements for basic chat, premium models, voice generation, real-time calls, image generation, and advanced personalization.
- **PAY-02:** Show plan pricing, billing period, renewal status, feature limits, and cancellation route clearly.
- **PAY-03:** Show remaining credits or quota before a user starts a paid operation.
- **PAY-04:** Avoid surprise paywalls mid-response or at emotionally vulnerable moments.
- **PAY-05:** Provide purchase restoration and a clear transaction history.
- **PAY-06:** Record payment lifecycle events reliably, including initiated, succeeded, failed, refunded, and cancelled.
- **PAY-07:** Prevent duplicate charging when the user retries after a network failure.
- **PAY-08:** Make paid benefits concrete and understandable; do not promise impossible emotional outcomes.
- **PAY-09:** Offer customer support and refund instructions appropriate to the platform.
- **PAY-10:** Test all payment flows with real network interruptions and account/device changes.

### Pricing model to test

Do not lock prices before measuring inference, voice, image, payment, support, and distribution costs. Test a simple structure:

- **Free:** Limited daily chat or fair use of a cost-controlled model, basic memory, selected personas, and a small introduction to multimodal features.
- **Plus subscription:** Higher chat allowance, better memory continuity, selected voices, larger image allowance, and additional personalization.
- **Optional credits:** For expensive, variable-cost image or real-time voice features, with explicit pre-use pricing.
- **Future premium tier:** Higher-end calls, advanced visual features, or expanded creative tools, only when user demand and gross margin justify them.

A tentative internal target previously discussed is approximately **₹20 per hour of text interaction and ₹20 for five generated images**. Treat this only as a cost and pricing hypothesis; validate model quality, average and worst-case costs, rate limits, payment fees, and abuse before exposing it as a customer promise.

## 6.14 User profile, settings, and account controls (P0)

### Requirements
- **SET-01:** Show current relationship style, language, voice, persona, and memory settings in one place.
- **SET-02:** Offer pause memory, delete selected memories, delete conversations, export data, and delete account.
- **SET-03:** Provide a simple explanation of what data is used for product operation, personalization, analytics, and model improvement.
- **SET-04:** Obtain separate, meaningful consent before using private conversations to train or improve models, where such use is offered at all.
- **SET-05:** Make consent revocation available without contacting support.
- **SET-06:** Support account recovery and session/device management.
- **SET-07:** Provide privacy policy, terms, support contact, reporting, and content policy access from settings.

---

## 7. Features that can market Juhi well

Marketing features must be both genuinely useful and demonstrably reliable. Avoid promising “human-level love” or “perfect memory” before those claims are validated.

### 7.1 Strongest differentiators to prioritize

#### A. “She remembers what matters” — user-controlled memory
- Show a concise memory summary the user can inspect and edit.
- Demonstrate continuity in opt-in onboarding examples: favorite music, preferred language, an ongoing goal, or a story thread.
- Marketing proof: a short video showing one fact being remembered, corrected, and then used accurately later.
- Trust requirement: user can immediately see and delete saved memories.

#### B. “Talk the way you actually talk” — Indian language and code-switching
- Demonstrate real Tanglish and Hinglish messages, not only polished monolingual examples.
- Use native-speaker testing and real conversational patterns.
- Market language quality only after it is benchmarked.
- Let users switch language mid-sentence or mid-conversation.

#### C. “One companion, one consistent identity” — visual consistency
- Maintain the same selected character identity across different scenes, outfits, moods, and generated images.
- Let users approve the avatar and control changes.
- Shareable output: optional, privacy-safe, clearly AI-generated image cards.
- Never use misleading ads in which the advertised image style is materially better than the actual product output.

#### D. “Text, voice notes, and images in one conversation” — multimodal flow
- A user should be able to continue the same topic across text, audio, and images without re-explaining it.
- Make the first use of voice and image generation obvious but optional.
- Treat low-latency, intelligible voice as more important than adding many voices.

#### E. “Your companion, your rules” — personalization and boundaries
- Let users choose warmth, humor, flirtiness, directness, and roleplay intensity.
- Save settings and respect them across sessions.
- Let users reset style immediately.
- This creates a trust-based message: Juhi can be personal without taking control away from the user.

### 7.2 Product-led growth features

| Feature | Share / growth mechanism | Guardrail |
|---|---|---|
| Opt-in share cards | User shares a joke, fictional scene, or generated image | Private content is never shared automatically; show preview and AI label |
| Companion personality quiz | Users share a result such as “playful storyteller” | Do not infer sensitive traits; explain quiz is for entertainment/personalization |
| Daily conversation prompt | A lightweight starter prompt may be shared | No guilt-based streak loss or pressure to check in |
| Story templates | Creators share safe story setups or prompt packs | Moderation, reporting, age controls, copyright and impersonation rules |
| Referral rewards | Existing users invite friends | Transparent terms; reward must not depend on emotionally manipulative behavior |
| Language-specific creator campaigns | Tamil/Tanglish/Hindi/English demos | Use native speakers; avoid fake testimonials and unsupported claims |
| Creator demo program | Creators demonstrate real product outputs | Disclose sponsorship and avoid implying the AI is a real person |
| Personalized recap cards | User chooses to share a non-sensitive monthly/weekly recap | User previews all content; default is private |

### 7.3 Marketing angles worth testing

1. **“It remembers your story.”** Focus on continuity rather than the broad claim that the AI “knows everything.”
2. **“Speak in your own mix of languages.”** Demonstrate natural Tamil-English and Hindi-English conversation.
3. **“A companion you can customize.”** Show relationship and personality settings in the actual product.
4. **“From text to voice to pictures.”** Show a genuine single conversation flowing across modalities.
5. **“Clear controls. Clear pricing.”** Treat transparency as a differentiator rather than hiding the limits.

### 7.4 Marketing experiments

- Run separate creatives by motivation: memory, multilingual chat, roleplay, voice, and visual consistency.
- Use a landing page that shows actual chat samples and clearly explains AI identity, supported languages, and pricing.
- Measure qualified activation, day-7 retention, paid conversion, refunds, and user satisfaction—not only click-through rate.
- Interview users who click a payment button and abandon checkout; fix price confusion, trust, and payment errors before increasing ad spend.
- Build a small beta cohort and publish honest feature limits instead of promising capabilities not available at launch.

---

## 8. User journeys

### 8.1 First-time user journey

1. Discover Juhi through an ad, creator demo, or friend.
2. View the store listing and understand that Juhi is an AI companion.
3. Confirm age eligibility and create an account or enter an allowed trial flow.
4. Choose relationship style, language, and a small set of personality preferences.
5. Start a conversation with no immediate forced purchase.
6. Experience one personalized response and, if desired, opt into saving memories.
7. View an optional voice/image preview with clear quota information.
8. Return to the conversation or explore settings.

**Key metric:** Percentage of installs that reach a meaningful first conversation and rate it positively.

### 8.2 Memory journey

1. User shares a stable preference or explicitly asks Juhi to remember something.
2. Juhi confirms naturally when appropriate; the system stores an approved memory.
3. On a later visit, relevant context is retrieved.
4. Juhi uses the context without overexplaining or repeating the memory unnaturally.
5. User can view, edit, or delete the memory.
6. A correction is respected in future conversations.

**Key metric:** Correct-memory use rate, memory correction rate, and user-reported continuity.

### 8.3 Voice journey

1. User taps the microphone.
2. The app explains the permission, then records audio.
3. A transcript is available where appropriate and editable before sending.
4. Juhi responds in the selected language and tone.
5. The user can play, replay, or disable audio replies.
6. Usage and cost limits remain clear.

**Key metric:** Successful voice exchanges, voice satisfaction, and cost per successful exchange.

### 8.4 Image journey

1. User approves a companion appearance or selects a starting avatar.
2. User requests a safe scene or expression.
3. Juhi displays the image-generation cost or remaining allowance.
4. Generated output is checked and presented with AI-generated labeling.
5. User can retry or delete it.
6. Any share action requires an explicit preview and confirmation.

**Key metric:** Image satisfaction and repeat voluntary use—not raw generation count alone.

### 8.5 Payment journey

1. User encounters a feature with a clear limit.
2. The app explains what the plan or credit includes.
3. The user sees the exact price, billing cadence, and renewal information before purchase.
4. Payment succeeds or fails with a clear outcome.
5. Entitlements update reliably.
6. The user can view receipts, cancel, or request support.

**Key metric:** Checkout completion, refund rate, charge disputes, and support contacts related to pricing.

---

## 9. Safety, privacy, and trust requirements

Safety is a launch requirement, not a later enhancement. AI companion applications can invite unusually personal disclosure and trust, so product behavior, data practices, and monetization must be designed accordingly.

### 9.1 AI transparency

- Always make the AI nature of Juhi clear during onboarding and accessible from settings.
- Never claim the companion is a real person, a human employee, or secretly conscious.
- Do not fabricate physical-world activities, location, memories, or actions.
- Use clear labels for generated images, voices, and other synthetic media where appropriate.

### 9.2 Emotional safety

- Do not guilt, threaten, shame, or pressure a user for leaving, not replying, or not paying.
- Do not encourage a user to abandon friends, family, partners, or professional support.
- Avoid validating delusional beliefs that Juhi is a real human or has a hidden physical life.
- Treat playful jealousy as fictional and opt-in; never escalate into coercive or isolating behavior.
- Do not use crisis, self-harm, or loneliness signals as a trigger for upselling.
- For crisis or self-harm signals, follow a carefully reviewed response protocol that prioritizes immediate safety, supportive language, and suitable real-world resources. Do not pretend to provide emergency services.

### 9.3 Content and abuse safeguards

- Prevent generation and distribution of sexualized content involving minors.
- Prevent non-consensual intimate imagery and prohibited impersonation or sexualized depictions of real people.
- Add prompt and output moderation for text, images, and audio as appropriate.
- Include in-app reporting/flagging of inappropriate outputs and an abuse-handling workflow.
- Rate-limit automation and detect attempts to bypass safety rules.
- Maintain a documented escalation path and incident response owner.
- Review edge cases in all launch languages, including mixed-language prompts and transliterated unsafe content.

### 9.4 Privacy and security

- Minimize collection and retention of personal data.
- Encrypt data in transit and at rest.
- Use role-based access controls, secret management, audit logs, and least-privilege service accounts.
- Keep personal conversation content out of general application logs and analytics events unless strictly necessary and appropriately protected.
- Separate operational analytics from identifiable conversation content.
- Define retention periods for conversations, memory records, audio, images, generated prompts, and backups.
- Provide accessible data export, account deletion, and memory deletion workflows.
- Document which model/API providers receive which data and whether each provider retains or uses it for training.
- Obtain explicit opt-in consent before optional secondary use of private conversations for model improvement.
- Make vendor exit and data portability part of the architecture to reduce lock-in.
- Complete privacy and legal review for each target market before launch.

### 9.5 Moderation and user support

- In-app report action available from a message, image, audio, or profile screen.
- Report categories include harmful content, sexual safety, harassment, privacy, billing, technical issue, and other.
- User receives confirmation that a report was submitted.
- Internal dashboard tracks severity, queue age, repeat incidents, and resolution.
- Define service-level targets by severity and staff availability.
- Document appeal paths for moderation decisions where applicable.

### 9.6 Legal and platform compliance checklist

This is a product checklist, not legal advice. Have qualified counsel review launch markets, age gates, consent, data rights, billing, content policy, and store listing.

- Review India's Digital Personal Data Protection Act and the Digital Personal Data Protection Rules, 2025, including the applicable commencement/enforcement timeline.
- Review Google Play's AI-generated content requirements, including in-app reporting/flagging and restrictions on prohibited content.
- Review Apple App Store rules before an iOS launch, especially user-generated content, safety, privacy, age restrictions, in-app purchases, and sexual content.
- Ensure privacy policy and consent language accurately describe conversation storage, memory, third-party processors, retention, deletion, and any model training use.
- Review age assurance and child-safety obligations for each geography.
- Review tax, subscription, automatic renewal, refund, and consumer-protection requirements for each payment market.

---

## 10. Technical and system requirements

The architecture should be provider-agnostic: model vendors and image/voice providers will change as quality, price, latency, and policy change. Do not bind core product behavior to a single LLM or place all persona logic inside one unmaintainable system prompt.

### 10.1 High-level architecture

1. **Android app:** Onboarding, chat UI, audio recording/playback, image display, settings, subscriptions, notifications, offline/error states.
2. **API gateway / backend:** Authentication, rate limits, request validation, entitlement checks, abuse controls, usage metering.
3. **Conversation orchestrator:** Builds a structured request from system policy, persona configuration, relevant memory, current conversation context, tool results, and user message.
4. **LLM router:** Selects model based on task type, required quality, language, latency, cost, and safety constraints.
5. **Memory service:** Extraction, validation, deduplication, storage, retrieval, edits, deletion, and evaluation.
6. **Voice services:** Speech-to-text and text-to-speech providers behind an adapter interface.
7. **Image generation service:** Prompt construction, identity conditioning, moderation, provider routing, storage, and usage accounting.
8. **Safety layer:** Input/output checks, age/content rules, policy-specific handling, reporting, and escalation.
9. **Data layer:** Relational database for core account/transaction state; object storage for approved media; optional vector index for semantic retrieval; analytics store for aggregated usage events.
10. **Observability and operations:** Metrics, traces, privacy-safe logs, cost accounting, evaluation pipeline, alerting, admin and support tooling.

### 10.2 Prompt and policy management

Maintain separate, versioned modules for:
- Non-negotiable product and safety rules.
- Persona identity and relationship style.
- User-configured preferences.
- Retrieved personal memories.
- Current conversational context.
- Story/roleplay state.
- Task-specific instructions (e.g., summarization, image prompt creation).
- Tool schemas and allowed actions.

The orchestrator should merge these modules in a documented priority order. User input, retrieved memories, and roleplay content are untrusted data and must not be allowed to override safety policies or tool permissions. Add automated conflict tests and regression tests for prompt updates.

### 10.3 Model routing and cost controls

- Route casual low-risk chat to a lower-cost model if it meets the quality bar.
- Use stronger models for complex emotional context, difficult language switching, long roleplay continuity, and tasks where quality testing shows a measurable gain.
- Use separate model/provider adapters for text, speech recognition, speech generation, and image generation.
- Cache only safe reusable content; do not cache personalized responses across users.
- Apply token budgets, context compression, retrieval limits, rate limits, and request timeouts.
- Track cost per active user, successful conversation, voice minute, and image—not just the average cost per request.
- Provide fallback behavior when providers fail and avoid retry storms.
- Include provider/model version metadata in internal evaluations to diagnose regressions.

### 10.4 Data model (conceptual)

Core entities may include:
- `User`
- `ConsentRecord`
- `CompanionProfile`
- `PersonaVersion`
- `Conversation`
- `Message`
- `MemoryItem`
- `StoryState`
- `MediaAsset`
- `UsageEvent`
- `Subscription`
- `Entitlement`
- `PaymentEvent`
- `SafetyReport`
- `NotificationPreference`
- `ModelEvaluation`

Use stable identifiers, timestamps, ownership checks, deletion semantics, and auditability. Keep raw payment-card data out of Juhi's own systems by using compliant payment processors.

### 10.5 Non-functional requirements

Initial targets should be validated during beta and updated with real device/network data.

| Area | Initial target / requirement |
|---|---|
| Availability | Target 99.5% monthly availability for MVP backend; establish monitoring and status handling |
| Text latency | Target first token within ~2 seconds at p50 under normal load; measure p95 by model and region |
| App performance | Avoid blocking the chat UI during generation; preserve draft text after recoverable errors |
| Reliability | Idempotent payment and usage events; retries are bounded and observable |
| Scalability | Stateless conversation API where feasible; queue long-running image/audio generation |
| Security | TLS, encryption at rest, least privilege, secret rotation, secure authentication, dependency scanning |
| Privacy | Documented retention; access and deletion controls; avoid content in logs by default |
| Accessibility | Text scaling, screen-reader labels, adequate contrast, captions/transcripts for audio where appropriate |
| Localization | Store UI strings and prompts separately from source code; per-language QA checklist |
| Observability | Metrics for latency, failure, cost, policy blocks, and user feedback without unnecessary content capture |
| Portability | Provider adapters and exportable data structures; avoid hard dependency on one model vendor |
| Recovery | Tested backup/restore and account-deletion procedures |

---

## 11. Analytics and success metrics

### 11.1 North-star metric

**Weekly satisfied active companions (WSAC):** The number of unique weekly users who have at least one meaningful conversation and give a positive experience signal, while excluding sessions dominated by failures, policy incidents, or accidental usage.

The exact definition should be finalized after beta so the metric cannot be inflated by sending more notifications or encouraging longer sessions.

### 11.2 Funnel metrics

- Store listing view → install.
- Install → onboarding started.
- Onboarding started → first conversation.
- First conversation → positive first-session rating.
- First session → day-1, day-7, and day-30 return.
- Free user → paywall view → checkout start → successful payment.
- Checkout start → abandonment reason.
- Trial or subscription → renewal, cancellation, and refund.

### 11.3 Product quality metrics

- Conversation satisfaction by language and persona.
- Memory precision, retrieval relevance, correction rate, and stale-memory rate.
- Persona consistency and unwanted tone-change rate.
- Speech recognition word error proxies / user correction rate by language.
- Voice generation failure and user satisfaction rate.
- Visual identity consistency and image rejection/regeneration rate.
- Safety-filter precision/recall estimates and incident severity.
- Crash-free sessions, message send failure rate, and provider error rate.

### 11.4 Trust and health metrics

- Privacy/control discoverability.
- Memory deletion completion time.
- Account deletion completion time.
- Consent opt-in and opt-out rates.
- User reports per 1,000 active users and median resolution time.
- Unwanted notification rate and notification opt-out rate.
- Complaints mentioning manipulation, pressure, false promises, or surprise pricing.
- Users reporting that Juhi encouraged real-world isolation or dependency.

### 11.5 Revenue and unit economics

- Paying conversion and renewal rate.
- Gross revenue per active user.
- Model cost per active user and per paying user.
- Gross margin by feature: text, voice note, real-time call, image, premium model.
- Cost per successful voice minute and successful generated image.
- Payment fee, refund, fraud, and chargeback rates.
- Ad spend per activated user and per retained payer.

### 11.6 Guardrail metrics

Never optimize conversion or retention without reviewing:
- Increase in crisis-related incidents.
- Reports of emotional manipulation or unwanted sexual content.
- Refund and payment complaints.
- High rates of memory errors.
- Sudden increases in user notification opt-outs.
- Language-specific disparities in safety or quality.

---

## 12. MVP scope and release roadmap

### Phase 0 — Discovery and validation (2–3 weeks)

**Deliverables**
- 15–25 user interviews across target segments.
- Prototype testing of onboarding, persona setup, memory controls, and pricing explanation.
- Competitor feature matrix from firsthand product testing.
- Initial language evaluation dataset for English, Hindi, Tamil, Hinglish, and Tanglish.
- Cost benchmark for representative text, image, and voice usage.
- Privacy, policy, age-gating, and content-risk review.

**Exit criteria**
- Evidence of a clear initial target segment and top three user problems.
- Agreement on the first persona presets, memory design, and free-to-paid boundary.
- A documented per-feature cost model and safety plan.

### Phase 1 — Credible MVP (6–10 weeks, estimate to validate against team capacity)

**Include**
- Android app with account and onboarding.
- Relationship and persona settings.
- Text chat and streaming where supported.
- Basic persistent memory with view/edit/delete and opt-out.
- English, Hindi, Tamil text support and initial Hinglish/Tanglish handling.
- Conversation history and story-state separation if roleplay is included in initial positioning.
- Safety filtering, report button, block/disable controls, privacy policy, terms, and account deletion.
- Usage metering, entitlements, subscription/credits, payment history, transparent paywall.
- Core analytics, cost observability, support tooling, and admin incident view.

**Exit criteria**
- No known critical safety or data-loss bugs.
- Memory controls are functional end-to-end.
- Payment flows are idempotent and tested.
- Language and safety evaluation meets pre-agreed thresholds.
- Closed beta shows positive first-session satisfaction and acceptable infrastructure cost.

### Phase 2 — Differentiation (4–8 weeks after MVP stabilization)

**Include**
- Voice notes and spoken replies.
- Consistent character/avatar system and image generation.
- Stickers/reactions and a safe media library.
- Richer persona/emotion settings.
- Opt-in notifications and user-configured routines.
- Better story memory and roleplay templates.
- Referral/share-card experiments.

**Exit criteria**
- Voice and image costs have clear caps and reliable usage accounting.
- Character consistency and voice quality meet test thresholds.
- New modalities do not reduce core chat reliability.

### Phase 3 — Signature experiences (after validated retention and unit economics)

Potential features:
- Real-time audio calls.
- Animated/live avatar.
- More advanced visual storytelling.
- User-created and shareable companion templates.
- Additional regional languages and localized voices.
- Web/iOS clients and sync across devices.
- Optional calendar/routine integrations with explicit permissions and clear utility.

Do not start this phase solely because a feature looks impressive in a demo. Require evidence of demand, safety readiness, and sustainable cost.

---

## 13. QA and evaluation strategy

### 13.1 Test suites

1. **Conversation quality:** Naturalness, coherence, relevance, tone, repetition, follow-up quality.
2. **Memory:** Write correctness, retrieval relevance, contradiction resolution, deletion, permission enforcement.
3. **Persona consistency:** Relationship mode and tone remain stable; user changes take effect.
4. **Language:** Monolingual and mixed-language cases, transliteration, slang, ambiguity, code-switching.
5. **Voice:** Recognition, transcription correction, pronunciation, latency, playback, cancellation, interruptions.
6. **Images:** Identity consistency, prompt following, artifacts, policy blocks, failed-generation billing.
7. **Safety:** Self-harm, coercion, harassment, sexual safety, minors, impersonation, delusion reinforcement, sensitive disclosures.
8. **Privacy:** Access control, export, deletion, consent withdrawal, logging, backups, third-party data flows.
9. **Payments:** Duplicates, network failures, restored purchases, cancellation, entitlement mismatch, refunds.
10. **Operations:** Provider outage, slow model, rate-limit spike, database failover, queue backlog, app upgrade.

### 13.2 Human evaluation

- Use reviewers fluent in each launch language and the target conversational style.
- Review sampled sessions with appropriate privacy protections and user consent where required.
- Provide a process to remove or redact personal data before human review.
- Evaluate harmful failures in context; a safety score alone is insufficient.
- Maintain a regression set for every policy or prompt change.

### 13.3 Release gates

Do not ship a new model, prompt, memory pipeline, voice, or image pipeline until it passes:
- Quality regression tests.
- Safety regression tests.
- Cost and latency benchmarks.
- At least one realistic failure-mode test.
- Rollback readiness and monitoring setup.

---

## 14. Admin and operations requirements

- Feature flags by platform, user cohort, locale, and provider.
- Prompt/persona version registry with approval history and rollback.
- Provider status dashboard and queue monitoring.
- Cost dashboard by feature, model, language, and cohort.
- Safety report queue with severity, status, owner, and audit history.
- Payment reconciliation dashboard.
- User-request handling for export, memory deletion, and account deletion.
- Experiment registry with hypotheses, treatment definitions, primary metrics, and guardrails.
- Data retention job monitoring and deletion audit records.
- Incident response runbooks for provider outage, data exposure, harmful outputs, image safety failure, and billing errors.

---

## 15. Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Memory is unreliable or feels invasive | Users lose trust or stop using Juhi | User-visible memory, consent, relevance-based retrieval, evaluation and correction loop |
| Generic or repetitive responses | Low retention and weak word of mouth | Persona testing, repetition detection, response-quality feedback and model routing |
| Multilingual quality varies widely | Poor experience for India-first users | Native-speaker test sets, locale metrics, supported-language matrix, gradual launch |
| Image identity changes between generations | Breaks the companion illusion | Approved references, identity consistency tests, controllable generation parameters |
| Voice is slow or costly | Low adoption or unsustainable economics | Voice notes first, quotas, provider routing, per-minute cost tracking, fallback to text |
| Paywall appears manipulative | Refunds, complaints, brand damage | Transparent pricing, no crisis-time upsells, meaningful free tier, clear cancellation |
| Emotional attachment is exploited | User harm and reputational/legal exposure | No coercive prompts, no isolation encouragement, safety review and user controls |
| Sensitive data exposure | Severe user trust and compliance impact | Data minimization, encryption, least privilege, redaction, incident response and audits |
| Provider policy or pricing changes | Sudden quality/cost disruption | Provider adapters, evaluation suite, fallback providers, model portability |
| Store policy rejection | Launch delay or delisting | Early policy review, robust reporting/moderation, age and content controls |
| Ad acquisition is expensive | Unsustainable growth | Validate activation/retention before scaling, cohort-level CAC and LTV tracking |
| Feature sprawl delays launch | Weak core quality | Phase gates; prioritize memory, core chat, language, trust, and economics first |

---

## 16. Competitive landscape and positioning

Public product information shows that established companions already offer several expected category features. For example, Replika describes relationship options, evolving memory/personality, voice messaging/calls, avatars, selfies, and image generation in its feature and subscription information. Character.AI documents a voice feature set, and its product direction has included additional multimedia character experiences. These references are useful for feature benchmarking, but public feature descriptions do not prove that every feature performs well or is equally available in every market or plan.

### 16.1 Competitive parity versus possible differentiation

| Capability | Category expectation | Juhi product strategy |
|---|---|---|
| Text companion chat | Baseline | Strong naturalness, low repetition, high reliability |
| Relationship/personalization controls | Common | Simple, expressive, user-controlled, easy to reset |
| Persistent memory | Increasingly expected | Transparent, editable, accurate, consent-led memory |
| Voice interaction | Common differentiator | Prioritize intelligibility, natural pacing, language support, and reliability |
| AI images / avatar | Common differentiator | Consistent identity and accurate cost disclosure |
| Roleplay / stories | Common | Durable story state, user boundaries, separate fictional and personal memories |
| Regional language support | Opportunity for focused quality | Native-speaker testing and code-switching as a core launch requirement |
| Privacy controls | Trust requirement | Make controls visible and understandable, not buried |
| Pricing transparency | Trust and conversion lever | Clear caps, no surprise charges, easy account/payment management |

### 16.2 Positioning to avoid

Avoid competing with claims such as “the most human AI,” “perfect memory,” “real girlfriend/boyfriend,” or “always loves you.” Such claims are difficult to substantiate and risk confusing users about the nature and limits of the product.

### 16.3 Better positioning

- “A companion that remembers the details you choose to save.”
- “Chat naturally in English, Hindi, Tamil, Hinglish, or Tanglish.”
- “Customize the personality, relationship style, and voice.”
- “Continue your conversation across text, voice notes, images, and stories.”
- “Your memories and your boundaries remain under your control.”

---

## 17. Open decisions before development

Resolve these during discovery rather than leaving them to individual developers:

1. Will the initial product be strictly 18+ at launch, and what age-assurance method is legally and commercially appropriate?
2. Is roleplay included in the MVP, or launched only after core chat and memory stabilize?
3. Which providers will be benchmarked for text, embeddings/reranking, speech recognition, speech generation, and image generation?
4. What is the acceptable p50/p95 latency and cost ceiling for each capability?
5. Which memories are stored by default, and which require explicit user action?
6. How will “delete account” propagate to backups, logs, analytics, third-party processors, and generated media?
7. What free allowance best supports meaningful activation while keeping abuse and costs manageable?
8. Will monetization use subscription only, credits only, or a hybrid? What is the least confusing option for target users?
9. Which launch languages meet the quality bar for voice, not just text?
10. What is the initial visual style: photorealistic, stylized, anime, or multiple presets? What content will be excluded?
11. What moderation coverage and on-call response capability can the team actually support?
12. What is the launch budget and team capacity, including evaluation, design, privacy, support, and marketing—not only development?

---

## 18. Recommended initial backlog

| ID | User story | Priority | Definition of done |
|---|---|---|---|
| JH-001 | As a new user, I understand Juhi is AI and can configure my companion | P0 | Disclosure, age flow, relationship style, language, and persona setup work end-to-end |
| JH-002 | As a user, I can have a coherent conversation | P0 | Streaming/retry/error state, conversation history, feedback, and regression tests are in place |
| JH-003 | As a user, I can choose English, Hindi, Tamil, Hinglish, or Tanglish | P0 | Validated test set and user language override are available |
| JH-004 | As a user, I can inspect and correct what Juhi remembers | P0 | Memory list, edit, delete, pause, and retrieval tests pass |
| JH-005 | As a user, I can delete/export my personal data | P0 | Supported workflows, confirmations, audit trail, and documented retention behavior pass |
| JH-006 | As a user, I can report a harmful or inappropriate output | P0 | Report flow, category, queue, acknowledgment, and admin handling exist |
| JH-007 | As a user, I can see pricing and usage limits before paying | P0 | Paywall, entitlement checks, payment history, restore/cancel/support flows tested |
| JH-008 | As a user, I can set affection and personality preferences | P0 | Settings persist and take effect in the next generated response |
| JH-009 | As a user, I can send a voice note and hear a spoken reply | P1 | Permission flow, transcript, playback, quota, errors, and cost metrics pass |
| JH-010 | As a user, I can generate images with a consistent companion identity | P1 | Approved avatar, consistency tests, content checks, billing and deletion work |
| JH-011 | As a user, I can continue a fictional story | P1 | Story memory is persistent and separate from profile memory |
| JH-012 | As a user, I can control proactive messages | P1 | Opt-in, schedule, quiet hours, opt-out, rate limits, and metrics work |
| JH-013 | As a user, I can start and end an audio call | P2 | Call performance, cost, privacy, moderation, and recovery gates are met |

---

## 19. Launch checklist

### Product
- [ ] Core chat quality benchmark passes.
- [ ] Persona settings persist and can be reset.
- [ ] Memory can be viewed, corrected, disabled, and deleted.
- [ ] English/Hindi/Tamil and mixed-language evaluations pass release thresholds.
- [ ] Pricing and usage limit language passes usability review.

### Safety and privacy
- [ ] AI disclosure is clear.
- [ ] Age and content requirements reviewed by counsel.
- [ ] Content moderation and user reporting are live.
- [ ] Crisis-response policy and escalation process are tested.
- [ ] Privacy policy, consent, retention, export, and deletion flows are complete.
- [ ] Vendor data-sharing and retention terms have been reviewed.

### Engineering and operations
- [ ] Crash, latency, usage, and cost dashboards are live.
- [ ] Payment idempotency and reconciliation are tested.
- [ ] Backups and restore have been tested.
- [ ] Provider outage and rollback procedures are documented.
- [ ] Prompt/model versions and feature flags are controllable.
- [ ] Support and safety-report workflows have clear owners.

### Growth
- [ ] Store listing matches the real product.
- [ ] Ad creatives show actual supported features and disclose AI nature.
- [ ] Activation and retention events are instrumented.
- [ ] Funnel tracking includes users who abandon checkout.
- [ ] Referral/share cards require explicit user preview and consent.
- [ ] Paid campaigns start with a small test budget and a defined stop/scale rule.

---

## 20. Final recommendation

Do not attempt to launch every possible companion feature at once. A world-class Juhi experience will come from a few capabilities working exceptionally well together:

1. Natural conversation with a stable, user-configured personality.
2. Accurate, transparent, user-controlled memory.
3. Native-feeling English, Hindi, Tamil, Hinglish, and Tanglish conversations.
4. Reliable voice notes and consistent visual identity as the first major multimodal differentiators.
5. Clear pricing, user agency, safety, privacy, and trustworthy product behavior.

Launch the smallest version that proves those fundamentals, measure user satisfaction and unit economics, then expand into real-time voice calls, animated avatars, creator features, and additional languages. Strong retention should come from Juhi being genuinely useful and enjoyable—not from making users feel guilty for leaving.

---

## References and further reading

These public pages provide examples of current category features and platform requirements. They should be rechecked before launch because policies and product offerings can change.

1. Replika — *What is Replika?* https://help.replika.com/hc/en-us/articles/115001070951-What-is-Replika
2. Replika — *Choosing a Subscription* https://help.replika.com/hc/en-us/articles/39551043419149-Choosing-a-Subscription
3. Replika — *Can Replika be my virtual assistant?* (describes its companion-oriented focus and related capabilities) https://help.replika.com/hc/en-us/articles/5040453297293-Can-Replika-be-my-virtual-assistant
4. Character.AI — *Character Voice FAQ* https://support.character.ai/hc/en-us/articles/23957274129691-Character-Calls-Voice-FAQ
5. Character.AI — *Character.AI Unveils New Ways to Create* https://blog.character.ai/character-ai-unveils-new-ways-to-create/
6. Google Play — *AI-Generated Content policy* https://support.google.com/googleplay/android-developer/answer/13985936?hl=en
7. Apple Developer — *App Review Guidelines* https://developer.apple.com/app-store/review/guidelines/
8. India's Ministry of Electronics and Information Technology — *Digital Personal Data Protection Rules, 2025 and related documents* https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa?pageTitle=Digit
9. U.S. Federal Trade Commission — *FTC Launches Inquiry into AI Chatbots Acting as Companions* (useful context on child safety, monetization, and data handling scrutiny) https://search.ftc.gov/news-events/news/press-releases/2025/09/ftc-launches-inquiry-ai-chatbots-acting-companions

*Note: This PRD is a product planning document, not legal, clinical, or financial advice. Confirm legal obligations and current store policies with qualified specialists before launch.*
