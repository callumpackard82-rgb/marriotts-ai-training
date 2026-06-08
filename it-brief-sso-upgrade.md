# IT Brief — Single Sign-On upgrade for the Staff AI Programme

**From:** [Your name], Head of AI
**To:** IT Lead / Network Manager (cc: Data Protection Officer)
**Date:** [date]
**Decision needed by:** [date]

## 1. What this is
The **Staff AI Programme** is an internal, self-paced training website for staff (live at
**https://marriotts-ai-training.netlify.app**). It is plain static HTML — no pupil data, no
logins, nothing stored on a server. Staff progress is currently saved only in the **browser on
the device they use** (`localStorage`).

## 2. The problem to solve
Because progress is per-device, a staff member who starts on a classroom PC can't see their
progress on their laptop or at home. **I'd like progress to follow the person across devices.**

## 3. What that requires
Cross-device personal progress needs two things we don't have today: (a) **sign-in** so the
system knows who each user is, and (b) **cloud storage** of progress against that identity. We
already have (a) — every staff member has a **Microsoft 365 / Entra ID** account — so this can be
**single sign-on** with no new passwords.

## 4. Recommended approach (Microsoft-native, low cost)
Move hosting to **Azure Static Web Apps** (Microsoft's own product, free tier ample for our size):

- Hosts the existing site **as-is** (no redesign).
- **Built-in Entra ID sign-in**, restricted to our tenant (only our staff can access).
- Stores each user's progress in a **SharePoint List in our own tenant** (preferred — keeps data
  in M365) or Azure Table Storage. Data per user is tiny: their identifier plus which modules
  they've completed and their preferred AI tool.
- Surfaced to staff via a **link/tab in Teams or SharePoint**, as now.

## 5. What I'm asking IT to do
1. Confirm/provide access to an **Azure subscription** (Static Web Apps free tier).
2. Approve an **Entra ID app registration** (or grant admin consent for the Static Web Apps
   built-in Entra provider) so staff can sign in with their school account.
3. Agree the **progress data store** — a SharePoint List in our tenant is my preference.
4. Restrict sign-in to **[school] tenant accounts only**.

I will handle (or arrange) the development work to connect the site to sign-in and storage — the
website itself is already built.

## 6. Data protection (for the DPO)
- **No pupil data, no special-category data.** The system stores only: the staff member's account
  identifier (e.g. email/object ID), module-completion flags, and a tool preference.
- All data stays **within our Microsoft 365 / Azure tenant** (data residency under existing
  agreements). No third-party processor beyond Microsoft.
- Low risk: recommend a short **DPIA screening** and adding this to the Record of Processing.
- This is a *privacy improvement* over today — progress data moves from uncontrolled local
  browsers into the managed tenant.

## 7. Cost & effort
- **Hosting:** Azure Static Web Apps **free tier** is expected to cover all staff (a few hundred
  users, minimal data).
- **Effort:** small — the front end exists; work is limited to wiring up authentication and
  read/write of progress.

## 8. Alternatives considered
- **Do nothing (keep per-device):** zero cost/effort, but no cross-device progress. *(Current state.)*
- **SharePoint List + sign-in, site hosted elsewhere:** similar to the recommendation; same IT asks.
- **Rebuild in Power Apps:** poor fit for the bespoke interactive lessons; more effort, no benefit.

## 9. Decision requested
Approval in principle for the **Azure Static Web Apps + Entra ID single sign-on** approach, and a
short call to confirm the four items in section 5.

---
*Background: the site is continuously deployed from GitHub (repo `marriotts-ai-training`) via
Netlify today; moving production to Azure Static Web Apps would not change the content, only the
host and the addition of sign-in.*
