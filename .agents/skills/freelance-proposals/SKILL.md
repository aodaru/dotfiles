# Freelance Proposal Writer

Skill for generating effective freelance proposals in Spanish and English based on job descriptions and templates.

## Commands

### Generate Proposal
`/propuesta "<job description>" [client-name]`

Generates a proposal in both Spanish and English. Automatically detects:
- Client name from description (if not provided)
- Tone (formal vs informal) based on job description style
- Project type and relevant experience to highlight

**Example:**
`/propuesta "Looking for a React developer to build an e-commerce dashboard. Need someone with 3+ years experience. Budget: $500. Timeline: 2 weeks." John`

### Generate with Portfolio Links
`/propuesta-con-links "<job description>" [client-name]`

Same as above but includes portfolio links (use only when client has contacted you first, not for initial proposals on Upwork/Workana).

### Analyze Job Description
`/analizar "<job description>"`

Extracts key requirements, technologies, budget, timeline, and suggests the best approach before writing the proposal.

**Example:**
`/analizar "Need WordPress expert to fix slow loading site. Currently taking 8 seconds. Must optimize images and database."`

### Study Past Proposals
`/estudio`

Analyzes your existing proposals in the examples folder and identifies successful patterns to incorporate.

## Template System

The skill uses four base templates:

1. **formal-es.md** - Formal Spanish
2. **formal-en.md** - Formal English
3. **informal-es.md** - Informal Spanish (casual grammar, tuteo)
4. **informal-en.md** - Informal English

### Template Variables

Templates support these variables that get replaced automatically:

- `{{CLIENT_NAME}}` - Client's name (extracted or provided)
- `{{PROJECT_TYPE}}` - Type of project detected
- `{{TECHNOLOGIES}}` - Relevant technologies mentioned
- `{{BUDGET}}` - Budget if mentioned
- `{{TIMELINE}}` - Timeline if mentioned
- `{{PORTFOLIO_LINKS}}` - Optional, only for /propuesta-con-links
- `{{BONUS_OFFER}}` - Optional discount for first clients

## Proposal Structure

All proposals follow this structure:

1. **Greeting** - Personalized with client's name + emoji
2. **Hook** - Acknowledge specific project details with enthusiasm
3. **Relevance** - Why you're perfect for this (experience match)
4. **Differentiation** - Bullet points of key strengths
5. **Portfolio** - Optional links (only with /propuesta-con-links)
6. **Approach** - How you'll tackle the project
7. **Timeline/Investment** - Estimated timeframe and rate (if appropriate)
8. **Questions** - 2-3 thoughtful questions to engage client
9. **CTA** - Strong call-to-action for next steps
10. **Closing** - Professional but warm sign-off

## Language Guidelines

### Spanish (Casual Style)
- Use "tú" form (tuteo) instead of "usted"
- Allow minor grammar "errors" for flow (missing accents, informal punctuation)
- Sound friendly and conversational like talking to a friend
- Example: "Hola Juan, cómo estás?" instead of "Estimado Sr. Juan"

### English
- Match the tone of the job description
- Use contractions for informal tone (I'm, don't, can't)
- Be enthusiastic but professional

## External Links Policy

**IMPORTANT:**
- `/propuesta` command: NO external links (safe for Upwork/Workana)
- `/propuesta-con-links` command: Includes portfolio links (use only after client contact)

## Learning from Examples

The skill learns from your existing proposals in the `examples/` folder:
- Your successful patterns
- Technologies you emphasize
- Your typical approach descriptions
- Your preferred closing style

## Best Practices

1. **Always personalize** with client's name
2. **Reference specific details** from the job description
3. **Show enthusiasm** for the project
4. **Include relevant experience** without being arrogant
5. **Ask questions** to start a conversation
6. **End with a clear next step** (call, chat, etc.)
7. **Keep it concise** - 150-250 words per language

## Example Outputs

### Input:
`/propuesta "Need a Laravel developer to build an API for a mobile app. We have 3 weeks and $800 budget. Experience with REST APIs required." Carlos`

### Output (Spanish):
```
👋Hola Carlos, cómo estás?

¡Este suena como un proyecto emocionante y las APIs REST son mi especialidad!

Con más de 12 años de experiencia en desarrollo web, incluyendo Laravel y APIs REST, estoy preparado para ayudarte a construir una API sólida para tu app móvil.

¿Y por qué deberías contratarme?

► He desarrollado múltiples APIs REST escalables que manejan miles de requests diarios
► Me gusta trabajar en equipo y mantener comunicación constante durante el desarrollo
► Soy independiente - una vez que entiendo los objetivos, ejecuto sin necesidad de micromanagement

Mi enfoque incluye: diseño de endpoints eficientes, documentación clara, y testing exhaustivo. Para un proyecto de esta magnitud, estimo unas 2-3 semanas.

Tengo algunas preguntas para asegurar el mejor resultado:
1. ¿Necesitas autenticación JWT o OAuth para la API?
2. ¿Ya tienes definidos los endpoints o necesitamos diseñarlos juntos?

¿Te gustaría charlar unos minutos esta semana para discutir los detalles? Estoy disponible para una videollamada cuando te convenga.

¡Que tengas un buen día!

- Adal
```

### Output (English):
```
👋Hi Carlos, how are you?

This sounds like an exciting project and REST APIs are my specialty!

With over 12 years of web development experience, including Laravel and REST APIs, I'm ready to help you build a solid API for your mobile app.

Why should you hire me?

► I've developed multiple scalable REST APIs handling thousands of daily requests
► I enjoy working in teams and maintaining constant communication throughout development
► I'm independent - once I understand the objectives, I execute without needing micromanagement

My approach includes: efficient endpoint design, clear documentation, and thorough testing. For a project of this scope, I estimate 2-3 weeks.

I have a few questions to ensure the best results:
1. Do you need JWT or OAuth authentication for the API?
2. Do you already have the endpoints defined or do we need to design them together?

Would you like to chat for a few minutes this week to discuss the details? I'm available for a video call whenever works for you.

Have a great day!

- Adal
```

## Configuration

Edit `config/user-profile.json` to customize:
- Your name/sign-off
- Default portfolio links (used with /propuesta-con-links)
- Your areas of expertise
- Typical rates
- Available time slots for calls

## Notes

- The skill automatically detects the best template (formal/informal) based on the job description's tone
- For translation jobs or writing tasks, the skill uses perfect grammar (override casual mode)
- Always review and customize before sending - this is a starting point, not final text
