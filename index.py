import os, re

# Load existing index.html if present, or reconstruct from the previous turn's verified HTML
if os.path.exists("index.html"):
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
else:
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Lead Tech Daily Field & Multi-Day Log</title>
  <link rel="icon" href="data:," />
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <style>
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    .tabular-nums {
      font-variant-numeric: tabular-nums;
    }
  </style>
</head>
<body class="bg-slate-100 text-slate-900 min-h-screen antialiased selection:bg-emerald-200 selection:text-slate-950">
  <div id="toastContainer" class="fixed top-4 right-4 z-50 flex flex-col gap-2 max-w-sm w-full pointer-events-none px-4 sm:px-0" aria-live="polite"></div>
  <div id="reconnectBanner" class="hidden sticky top-0 z-40 bg-emerald-700 text-white border-b border-emerald-800 shadow-md" role="status">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-2.5 flex flex-wrap items-center justify-between gap-3">
      <div class="flex items-center gap-2.5 text-xs sm:text-sm font-semibold">
        <span class="inline-flex h-2.5 w-2.5 rounded-full bg-emerald-300 animate-pulse"></span>
        <span id="reconnectMessage">Connection restored. Queued reports are ready to send.</span>
      </div>
      <div class="flex items-center gap-2">
        <button type="button" id="bannerOpenEmailBtn" class="px-3 py-1.5 rounded-lg bg-white text-emerald-950 hover:bg-emerald-50 text-xs font-bold transition cursor-pointer">Open Email</button>
        <button type="button" id="dismissReconnectBtn" class="px-2.5 py-1.5 rounded-lg bg-emerald-800/80 hover:bg-emerald-800 text-xs font-semibold text-emerald-100 transition cursor-pointer">Dismiss</button>
      </div>
    </div>
  </div>
  <header class="bg-slate-900 text-white border-b border-slate-800 shadow-sm">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-4 flex flex-wrap items-center justify-between gap-3">
      <div class="min-w-0">
        <div class="flex items-center gap-2">
          <span class="inline-block w-2.5 h-2.5 rounded-full bg-emerald-400 shrink-0"></span>
          <span class="text-xs font-semibold uppercase tracking-widest text-emerald-400">Field Operations &bull; Offline Resilient &bull; Multi-Day Ready</span>
        </div>
        <h1 class="text-xl sm:text-2xl font-extrabold tracking-tight mt-0.5 truncate">Lead Tech Daily Field Checklist</h1>
      </div>
      <div class="flex flex-wrap items-center gap-2 sm:gap-2.5">
        <div class="inline-flex rounded-xl bg-slate-800 p-1 border border-slate-700" role="tablist" aria-label="Workspace View">
          <button type="button" id="tabFieldFormBtn" role="tab" aria-selected="true" class="px-3 py-1 rounded-lg text-xs font-bold bg-emerald-500 text-slate-950 transition cursor-pointer">Field Checklist</button>
          <button type="button" id="tabPmSummaryBtn" role="tab" aria-selected="false" class="px-3 py-1 rounded-lg text-xs font-bold text-slate-300 hover:text-white transition cursor-pointer">PM Summary</button>
        </div>
        <div id="connectivityPill" title="Current network connection state" class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-bold border transition bg-emerald-950/80 text-emerald-300 border-emerald-700/70">
          <span id="connectivityDot" class="w-2 h-2 rounded-full bg-emerald-400"></span>
          <span id="connectivityLabel">Online</span>
        </div>
        <button type="button" id="headerQueueBadgeBtn" title="Jump to Offline Report Queue" class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-bold bg-amber-500/15 hover:bg-amber-500/25 text-amber-300 border border-amber-400/40 transition cursor-pointer tabular-nums">
          <span>Queue:</span>
          <span id="headerQueueCount" class="px-1.5 py-0.5 rounded-full bg-amber-400 text-slate-950 font-extrabold leading-none">0</span>
        </button>
      </div>
    </div>
  </header>
  <main class="max-w-5xl mx-auto px-4 sm:px-6 py-6 space-y-6">
    <div id="fieldChecklistView" class="space-y-6">
      <section class="bg-white rounded-2xl shadow-sm border border-slate-200/90 overflow-hidden">
        <div class="px-5 py-3.5 bg-slate-50 border-b border-slate-200/80 flex flex-wrap items-center justify-between gap-2">
          <div class="flex items-center gap-2">
            <span class="w-6 h-6 rounded-lg bg-slate-900 text-white text-xs font-bold flex items-center justify-center">1</span>
            <h2 class="text-sm font-bold uppercase tracking-wider text-slate-700">Recipient, Auto Time &amp; Assignment</h2>
          </div>
          <span id="draftSaveBadge" class="text-[11px] font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2.5 py-0.5 rounded-full">Draft saved in localStorage</span>
        </div>
        <div class="p-5 space-y-5">
          <div>
            <div class="flex items-center justify-between gap-2 mb-1.5">
              <label for="recipientEmail" class="block text-xs font-bold uppercase tracking-wide text-slate-600">Recipient Email <span class="text-rose-600">*</span></label>
              <span class="text-[11px] font-semibold text-slate-500">Required &bull; Saved in localStorage</span>
            </div>
            <input type="email" id="recipientEmail" value="" required placeholder="Enter recipient email address..." class="w-full rounded-xl border border-slate-300 bg-white px-3.5 py-2.5 text-sm font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-900 focus:border-slate-900 transition" />
            <p id="recipientEmailError" class="hidden mt-1 text-xs font-semibold text-rose-600">Please enter a valid recipient email address before emailing, copying, or queueing a report.</p>
            <p class="text-[11px] text-slate-500 mt-1.5">Enter the email address to send to. Your entry is saved automatically in <code class="text-slate-700">localStorage</code> and used for <code class="text-slate-700">mailto:</code> and reports.</p>
          </div>
          <div class="bg-sky-50/60 border border-sky-200/80 rounded-xl p-3.5">
            <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold uppercase tracking-wider text-sky-900">Auto Time</span>
                <span id="liveClockBadge" class="text-[11px] font-mono font-semibold text-sky-800 bg-sky-100 border border-sky-200 px-2 py-0.5 rounded-full tabular-nums">Clock: --:--:--</span>
              </div>
              <button type="button" id="refreshTimestampBtn" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold bg-sky-700 hover:bg-sky-800 active:scale-[0.99] text-white shadow-2xs transition cursor-pointer">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
                <span>Refresh Time</span>
              </button>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label for="autoTimeDisplay" class="block text-[11px] font-bold uppercase tracking-wider text-slate-600 mb-1">Captured Auto Time</label>
                <input type="text" id="autoTimeDisplay" readonly class="w-full rounded-xl border border-sky-200 bg-white px-3.5 py-2 text-xs sm:text-sm font-mono font-semibold text-slate-800 tabular-nums focus:outline-none" />
              </div>
              <div>
                <label for="reportDate" class="block text-[11px] font-bold uppercase tracking-wider text-slate-600 mb-1">Report Date</label>
                <input type="date" id="reportDate" class="w-full rounded-xl border border-slate-300 bg-white px-3.5 py-2 text-xs sm:text-sm font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-900 focus:border-slate-900 transition" />
              </div>
            </div>
            <p id="timestampMetaText" class="text-[11px] text-slate-500 mt-1.5">Automatically captured on load. Click Refresh Time anytime to stamp the current time.</p>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label for="dcSelect" class="block text-xs font-bold uppercase tracking-wide text-slate-600 mb-1.5">DC Selector <span class="text-rose-600">*</span></label>
              <select id="dcSelect" required class="w-full rounded-xl border border-slate-300 bg-white px-3.5 py-3 text-sm font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-900 focus:border-slate-900 transition">
                <option value="" disabled selected>Select DC...</option>
                <option value="DC1 Temp Camera">DC1 Temp Camera</option>
                <option value="DC1 TFO">DC1 TFO</option>
                <option value="DC2 Temp Camera">DC2 Temp Camera</option>
                <option value="DC2 TFO">DC2 TFO</option>
                <option value="DC4 Temp Camera">DC4 Temp Camera</option>
                <option value="DC4 TFO">DC4 TFO</option>
                <option value="DC5 Temp Camera">DC5 Temp Camera</option>
                <option value="DC5 TFO">DC5 TFO</option>
                <option value="DC6 Temp Camera">DC6 Temp Camera</option>
                <option value="DC6 TFO">DC6 TFO</option>
                <option value="DC7 Base Build">DC7 Base Build</option>
                <option value="DC7 TFO">DC7 TFO</option>
              </select>
              <p id="dcError" class="hidden mt-1 text-xs font-semibold text-rose-600">Please select a DC from DC Selector.</p>
            </div>
            <div>
              <label for="techSelect" class="block text-xs font-bold uppercase tracking-wide text-slate-600 mb-1.5">Tech Name <span class="text-rose-600">*</span></label>
              <select id="techSelect" required class="w-full rounded-xl border border-slate-300 bg-white px-3.5 py-3 text-sm font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-900 focus:border-slate-900 transition">
                <option value="" disabled selected>Select Tech...</option>
                <option value="Tyler">Tyler</option>
                <option value="Gabe">Gabe</option>
                <option value="Andrew">Andrew</option>
              </select>
              <p id="techError" class="hidden mt-1 text-xs font-semibold text-rose-600">Please select a Tech Name.</p>
            </div>
          </div>
          <div>
            <label for="installTypeSelect" class="block text-xs font-bold uppercase tracking-wide text-slate-600 mb-1.5">Installation Type <span class="text-rose-600">*</span></label>
            <div class="relative">
              <select id="installTypeSelect" required class="w-full appearance-none rounded-xl border-2 border-slate-800 bg-slate-900 text-white px-3.5 py-3 pr-10 text-sm font-bold focus:outline-none focus:ring-2 focus:ring-emerald-500 transition shadow-sm">
                <option value="" disabled selected>Select Installation Type...</option>
                <option value="Access Wire Pull">Access Wire Pull</option>
                <option value="ADO Wire Pull">ADO Wire Pull</option>
                <option value="Security Rack Wire Pull">Security Rack Wire Pull</option>
                <option value="Door">Door</option>
                <option value="Camera">Camera</option>
                <option value="Intercom">Intercom</option>
              </select>
              <svg class="w-4 h-4 text-emerald-400 pointer-events-none absolute right-3.5 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" /></svg>
            </div>
            <p id="installTypeError" class="hidden mt-1 text-xs font-semibold text-rose-600">Please select an Installation Type.</p>
          </div>
        </div>
      </section>
      <section id="deviceLocationSection" class="bg-white rounded-2xl shadow-sm border border-slate-200/90 overflow-hidden">
        <div class="px-5 py-3.5 bg-slate-50 border-b border-slate-200/80 flex flex-wrap items-center justify-between gap-2">
          <div class="flex items-center gap-2">
            <span class="w-6 h-6 rounded-lg bg-slate-900 text-white text-xs font-bold flex items-center justify-center">2</span>
            <h2 class="text-sm font-bold uppercase tracking-wider text-slate-700">Device, Location &amp; Multi-Day Job Log</h2>
          </div>
          <span class="text-xs font-bold text-rose-700 bg-rose-50 border border-rose-200 px-2.5 py-0.5 rounded-full">Device &amp; Location Required</span>
        </div>
        <div class="p-5 space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label for="deviceNameInput" class="block text-xs font-bold uppercase tracking-wide text-slate-600 mb-1.5">Device Name <span class="text-rose-600">*</span></label>
              <input type="text" id="deviceNameInput" required placeholder="Enter Device Name" class="w-full rounded-xl border border-slate-300 bg-white px-3.5 py-3 text-sm font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-900 focus:border-slate-900 transition" />
              <p id="deviceNameError" class="hidden mt-1 text-xs font-semibold text-rose-600">Device Name is required before emailing, copying, or queueing a report.</p>
            </div>
            <div>
              <label for="locationInput" class="block text-xs font-bold uppercase tracking-wide text-slate-600 mb-1.5">Location <span class="text-rose-600">*</span></label>
              <input type="text" id="locationInput" required placeholder="Enter Location" class="w-full rounded-xl border border-slate-300 bg-white px-3.5 py-3 text-sm font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-900 focus:border-slate-900 transition" />
              <p id="locationError" class="hidden mt-1 text-xs font-semibold text-rose-600">Location is required before emailing, copying, or queueing a report.</p>
            </div>
          </div>
          <div class="bg-slate-50 border border-slate-200/90 rounded-xl p-3.5 space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <span class="text-xs font-bold uppercase tracking-wider text-slate-700">Multi-Day Install Tracking <span class="text-[11px] font-medium normal-case text-slate-500">(Optional for PM / Job Costing)</span></span>
              <span class="text-[11px] font-semibold text-slate-500">Helps roll up multi-day progress</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-4 gap-3">
              <div>
                <label for="jobRefInput" class="block text-[11px] font-bold uppercase tracking-wider text-slate-600 mb-1">Job / WO #</label>
                <input type="text" id="jobRefInput" placeholder="e.g. WO-4082" class="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-xs sm:text-sm font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-900 transition" />
              </div>
              <div>
                <label for="phaseSelect" class="block text-[11px] font-bold uppercase tracking-wider text-slate-600 mb-1">Install Phase</label>
                <select id="phaseSelect" class="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-xs sm:text-sm font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-900 transition">
                  <option value="">Select Phase...</option>
                  <option value="Rough-In / Wire Pull">Rough-In / Wire Pull</option>
                  <option value="Trim / Hardware Mount">Trim / Hardware Mount</option>
                  <option value="Termination / IP / Program">Termination / IP / Program</option>
                  <option value="Testing / Commissioning">Testing / Commissioning</option>
                </select>
              </div>
              <div>
                <label for="hoursWorkedInput" class="block text-[11px] font-bold uppercase tracking-wider text-slate-600 mb-1">Hours Today</label>
                <input type="number" id="hoursWorkedInput" min="0" max="24" step="0.25" placeholder="0.0" class="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-xs sm:text-sm font-semibold text-slate-900 tabular-nums placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-900 transition" />
              </div>
              <div>
                <label for="blockerSelect" class="block text-[11px] font-bold uppercase tracking-wider text-slate-600 mb-1">Blocker / Hold Status</label>
                <select id="blockerSelect" class="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-xs sm:text-sm font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-900 transition">
                  <option value="None - On Track">None - On Track</option>
                  <option value="Waiting on GC / Drywall / Paint">Waiting on GC / Drywall / Paint</option>
                  <option value="Waiting on Parts / Materials">Waiting on Parts / Materials</option>
                  <option value="Access / Escort / Lift Needed">Access / Escort / Lift Needed</option>
                  <option value="Network / IP / Head-End Pending">Network / IP / Head-End Pending</option>
                </select>
              </div>
            </div>
          </div>
          <div id="deviceLocationFeedback" class="hidden rounded-xl border border-rose-200 bg-rose-50 px-3.5 py-2.5 text-xs font-semibold text-rose-700"></div>
        </div>
      </section>
      <section id="checklistSection" class="bg-white rounded-2xl shadow-sm border border-slate-200/90 overflow-hidden">
        <div class="px-5 py-3.5 bg-slate-50 border-b border-slate-200/80 flex flex-wrap items-center justify-between gap-2.5">
          <div class="flex items-center gap-2">
            <span class="w-6 h-6 rounded-lg bg-slate-900 text-white text-xs font-bold flex items-center justify-center">3</span>
            <h2 class="text-sm font-bold uppercase tracking-wider text-slate-700">Checklist Questions <span id="activeBranchTag" class="hidden ml-1.5 px-2 py-0.5 rounded-md text-xs font-bold bg-slate-900 text-emerald-400 normal-case"></span></h2>
            <span id="branchRequiredBadge" class="hidden text-[11px] font-bold text-rose-700 bg-rose-50 border border-rose-200 px-2 py-0.5 rounded-full">All Required</span>
          </div>
          <div class="flex flex-wrap items-center gap-2.5">
            <div class="flex items-center gap-2">
              <span id="completionText" class="text-xs font-bold text-slate-700 tabular-nums">0% (0/0 Yes)</span>
              <div class="w-24 sm:w-28 h-2.5 bg-slate-200 rounded-full overflow-hidden">
                <div id="completionBar" class="h-full bg-emerald-500 transition-all duration-300 rounded-full" style="width: 0%"></div>
              </div>
            </div>
            <button type="button" id="completedToggleBtn" aria-pressed="false" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold border transition cursor-pointer bg-white text-slate-700 border-slate-300 hover:bg-slate-100">
              <span id="completedCheckBox" class="w-4 h-4 rounded border border-slate-400 flex items-center justify-center text-[11px] leading-none bg-white text-transparent">&#10003;</span>
              <span>Completed</span>
            </button>
          </div>
        </div>
        <div class="p-5">
          <div id="emptyQuestionsState" class="text-center py-9 px-4 border-2 border-dashed border-slate-200 rounded-xl bg-slate-50/60">
            <p class="text-sm font-semibold text-slate-600">Select an Installation Type above.</p>
            <p class="text-xs text-slate-400 mt-1">Required checklist questions for the chosen Installation Type will appear here.</p>
          </div>
          <div id="questionsContainer" class="space-y-3 hidden"></div>
          <div id="questionsValidationFeedback" class="hidden mt-3 rounded-xl border border-rose-200 bg-rose-50 px-3.5 py-2.5 text-xs font-semibold text-rose-700"></div>
          <div class="mt-5 pt-4 border-t border-slate-100">
            <label for="notesInput" class="block text-xs font-bold uppercase tracking-wide text-slate-600 mb-1.5">Notes <span class="text-[11px] font-medium normal-case text-slate-400">(Optional)</span></label>
            <textarea id="notesInput" rows="3" placeholder="Optional notes, blockers, wire/part details, or multi-day handoff notes..." class="w-full rounded-xl border border-slate-300 bg-white px-3.5 py-2.5 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-900 focus:border-slate-900 transition"></textarea>
          </div>
        </div>
      </section>
      <section class="bg-white rounded-2xl shadow-sm border border-slate-200/90 overflow-hidden">
        <div class="px-5 py-3.5 bg-slate-50 border-b border-slate-200/80 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-6 h-6 rounded-lg bg-slate-900 text-white text-xs font-bold flex items-center justify-center">4</span>
            <h2 class="text-sm font-bold uppercase tracking-wider text-slate-700">Report Preview &amp; Actions</h2>
          </div>
          <span class="text-[11px] font-semibold text-slate-500">Live summary</span>
        </div>
        <div class="p-5 space-y-4">
          <div class="rounded-xl bg-slate-900 text-slate-100 p-4 font-mono text-xs sm:text-[13px] leading-relaxed overflow-x-auto border border-slate-800 shadow-inner">
            <div class="pb-2.5 mb-2.5 border-b border-slate-800 space-y-1">
              <div class="flex gap-2"><span class="text-slate-400 select-none shrink-0">To:</span><span id="previewTo" class="text-emerald-400 font-semibold break-all">[Required]</span></div>
              <div class="flex gap-2"><span class="text-slate-400 select-none shrink-0">Subject:</span><span id="previewSubject" class="text-amber-300 font-semibold break-words">[Lead Tech Daily Field Checklist] ...</span></div>
            </div>
            <pre id="previewBody" class="whitespace-pre-wrap break-words text-slate-200 font-mono text-xs sm:text-[13px]"></pre>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-1">
            <button type="button" id="openEmailBtn" class="w-full inline-flex items-center justify-center gap-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 active:scale-[0.99] text-white font-bold text-sm px-4 py-3.5 shadow-sm transition cursor-pointer">
              <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
              <span>Open Email</span>
            </button>
            <button type="button" id="copyReportBtn" class="w-full inline-flex items-center justify-center gap-2 rounded-xl bg-slate-900 hover:bg-slate-800 active:scale-[0.99] text-white font-bold text-sm px-4 py-3.5 shadow-sm transition cursor-pointer">
              <svg id="copyIconDefault" class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
              <svg id="copyIconSuccess" class="w-4 h-4 shrink-0 hidden text-emerald-400" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" /></svg>
              <span id="copyBtnLabel">Copy Report</span>
            </button>
            <button type="button" id="queueOfflineReportBtn" class="w-full inline-flex items-center justify-center gap-2 rounded-xl bg-amber-500 hover:bg-amber-400 active:scale-[0.99] text-slate-950 font-bold text-sm px-4 py-3.5 shadow-sm transition cursor-pointer">
              <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" /></svg>
              <span>Queue / Save Offline Report</span>
            </button>
          </div>
        </div>
      </section>
    </div>
    <div id="pmSummaryView" class="hidden space-y-6">
      <section class="bg-white rounded-2xl shadow-sm border border-slate-200/90 overflow-hidden">
        <div class="px-5 py-3.5 bg-slate-50 border-b border-slate-200/80 flex flex-wrap items-center justify-between gap-2">
          <div class="flex items-center gap-2">
            <span class="w-6 h-6 rounded-lg bg-slate-900 text-white text-xs font-bold flex items-center justify-center">PM</span>
            <h2 class="text-sm font-bold uppercase tracking-wider text-slate-700">Multi-Day &amp; Queued Report Roll-Up</h2>
          </div>
          <span class="text-[11px] font-semibold text-slate-500">Local Roll-Up (No SQL Server Required)</span>
        </div>
        <div class="p-5 space-y-5">
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <label for="pmFilterDc" class="block text-[11px] font-bold uppercase tracking-wider text-slate-600 mb-1">Filter by DC</label>
              <select id="pmFilterDc" class="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-xs sm:text-sm font-semibold text-slate-900">
                <option value="ALL">All DCs</option>
                <option value="DC1 Temp Camera">DC1 Temp Camera</option>
                <option value="DC1 TFO">DC1 TFO</option>
                <option value="DC2 Temp Camera">DC2 Temp Camera</option>
                <option value="DC2 TFO">DC2 TFO</option>
                <option value="DC4 Temp Camera">DC4 Temp Camera</option>
                <option value="DC4 TFO">DC4 TFO</option>
                <option value="DC5 Temp Camera">DC5 Temp Camera</option>
                <option value="DC5 TFO">DC5 TFO</option>
                <option value="DC6 Temp Camera">DC6 Temp Camera</option>
                <option value="DC6 TFO">DC6 TFO</option>
                <option value="DC7 Base Build">DC7 Base Build</option>
                <option value="DC7 TFO">DC7 TFO</option>
              </select>
            </div>
            <div>
              <label for="pmFilterTech" class="block text-[11px] font-bold uppercase tracking-wider text-slate-600 mb-1">Filter by Tech</label>
              <select id="pmFilterTech" class="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-xs sm:text-sm font-semibold text-slate-900">
                <option value="ALL">All Techs</option>
                <option value="Tyler">Tyler</option>
                <option value="Gabe">Gabe</option>
                <option value="Andrew">Andrew</option>
              </select>
            </div>
            <div>
              <label for="pmFilterStatus" class="block text-[11px] font-bold uppercase tracking-wider text-slate-600 mb-1">Filter by Status / Blockers</label>
              <select id="pmFilterStatus" class="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-xs sm:text-sm font-semibold text-slate-900">
                <option value="ALL">All Reports</option>
                <option value="COMPLETED">Completed Only</option>
                <option value="INCOMPLETE">Not Completed</option>
                <option value="BLOCKED">Blocked / On Hold Only</option>
              </select>
            </div>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div class="rounded-xl border border-slate-200 bg-slate-50 p-3.5">
              <div class="text-[11px] font-bold uppercase tracking-wider text-slate-500">Filtered Reports</div>
              <div id="pmKpiCount" class="text-2xl font-extrabold text-slate-900 mt-1 tabular-nums">0</div>
            </div>
            <div class="rounded-xl border border-emerald-200 bg-emerald-50/70 p-3.5">
              <div class="text-[11px] font-bold uppercase tracking-wider text-emerald-700">Completed</div>
              <div id="pmKpiCompleted" class="text-2xl font-extrabold text-emerald-900 mt-1 tabular-nums">0</div>
            </div>
            <div class="rounded-xl border border-sky-200 bg-sky-50/70 p-3.5">
              <div class="text-[11px] font-bold uppercase tracking-wider text-sky-700">Logged Hours</div>
              <div id="pmKpiHours" class="text-2xl font-extrabold text-sky-900 mt-1 tabular-nums">0.0</div>
            </div>
            <div class="rounded-xl border border-amber-200 bg-amber-50/70 p-3.5">
              <div class="text-[11px] font-bold uppercase tracking-wider text-amber-800">Blockers / Holds</div>
              <div id="pmKpiBlockers" class="text-2xl font-extrabold text-amber-950 mt-1 tabular-nums">0</div>
            </div>
          </div>
          <div class="overflow-x-auto rounded-xl border border-slate-200">
            <table class="min-w-full divide-y divide-slate-200 text-xs sm:text-sm">
              <thead class="bg-slate-900 text-white text-left text-xs uppercase tracking-wider">
                <tr>
                  <th class="px-3.5 py-2.5">DC</th>
                  <th class="px-3.5 py-2.5">Device / WO</th>
                  <th class="px-3.5 py-2.5">Phase</th>
                  <th class="px-3.5 py-2.5">Tech</th>
                  <th class="px-3.5 py-2.5">Hours</th>
                  <th class="px-3.5 py-2.5">Blocker / Status</th>
                </tr>
              </thead>
              <tbody id="pmSummaryTableBody" class="divide-y divide-slate-200 bg-white">
                <tr>
                  <td colspan="6" class="px-4 py-6 text-center text-slate-500">Queue reports in the Field Checklist tab to see multi-day roll-ups here.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>
    <section id="offlineQueueSection" class="bg-white rounded-2xl shadow-sm border border-slate-200/90 overflow-hidden">
      <div class="px-5 py-3.5 bg-slate-50 border-b border-slate-200/80 flex flex-wrap items-center justify-between gap-2">
        <div class="flex items-center gap-2">
          <span class="w-6 h-6 rounded-lg bg-amber-500 text-slate-950 text-xs font-extrabold flex items-center justify-center tabular-nums"><span id="queueSectionBadgeCount">0</span></span>
          <h2 class="text-sm font-bold uppercase tracking-wider text-slate-700">Offline Report Queue</h2>
        </div>
        <div class="flex flex-wrap items-center gap-1.5 sm:gap-2">
          <button type="button" id="downloadQueueTxtBtn" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-800 hover:bg-slate-900 disabled:opacity-40 disabled:cursor-not-allowed text-white transition cursor-pointer">Download .txt</button>
          <button type="button" id="clearAllQueueBtn" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-rose-50 hover:bg-rose-100 disabled:opacity-40 disabled:cursor-not-allowed text-rose-700 border border-rose-200 transition cursor-pointer">Clear All</button>
        </div>
      </div>
      <div class="p-5">
        <div id="offlineQueueEmpty" class="text-center py-7 px-4 border-2 border-dashed border-slate-200 rounded-xl bg-slate-50/60">
          <p class="text-sm font-semibold text-slate-600">No reports in Offline Report Queue.</p>
          <p class="text-xs text-slate-400 mt-1">Use <span class="font-semibold text-slate-600">Queue / Save Offline Report</span> to store reports locally in <code class="text-slate-600">localStorage</code>.</p>
        </div>
        <div id="offlineQueueList" class="space-y-3 hidden"></div>
      </div>
    </section>
  </main>
  <script>
    const DEFAULT_RECIPIENT_EMAIL = '';
    const STORAGE_KEY_EMAIL = 'lead_tech_checklist_recipient_email_v1';
    const STORAGE_KEY_DRAFT = 'lead_tech_checklist_draft_v2';
    const STORAGE_KEY_QUEUE = 'lead_tech_checklist_queue_v2';

    const CHECKLIST_QUESTIONS = {
      'Access Wire Pull': [{ id: 'awp_1', label: 'Is string in pathway?', options: ['Yes', 'No'] }],
      'ADO Wire Pull': [{ id: 'ado_1', label: 'Is string in pathway?', options: ['Yes', 'No'] }],
      'Security Rack Wire Pull': [{ id: 'srwp_1', label: 'Is string in pathway?', options: ['Yes', 'No'] }],
      'Door': [
        { id: 'door_1', label: 'Is drywall installed?', options: ['Yes', 'No'] },
        { id: 'door_2', label: 'Is wall painted?', options: ['Yes', 'No'] },
        { id: 'door_3', label: 'Is Access Wire pulled?', options: ['Yes', 'No'] },
        { id: 'door_4', label: 'Is CR installed?', options: ['Yes', 'No'] },
        { id: 'door_5', label: 'Is BR installed?', options: ['Yes', 'No'] },
        { id: 'door_6', label: 'Is sounder installed?', options: ['Yes', 'No'] },
        { id: 'door_7', label: 'Is DC installed?', options: ['Yes', 'No'] },
        { id: 'door_8', label: 'Is REX and lock terminated?', options: ['Yes', 'No'] },
        { id: 'door_9', label: 'If BR is present, is it programmed?', options: ['Yes', 'No', 'N/A'] }
      ],
      'Camera': [
        { id: 'cam_1', label: 'Is J-box installed?', options: ['Yes', 'No'] },
        { id: 'cam_2', label: 'Is mud ring installed?', options: ['Yes', 'No'] },
        { id: 'cam_3', label: 'Is Cat6 pulled?', options: ['Yes', 'No'] },
        { id: 'cam_4', label: 'Is camera installed?', options: ['Yes', 'No'] },
        { id: 'cam_5', label: 'Is camera IPed?', options: ['Yes', 'No'] }
      ],
      'Intercom': [
        { id: 'int_1', label: 'Is drywall installed?', options: ['Yes', 'No'] },
        { id: 'int_2', label: 'Is wall painted?', options: ['Yes', 'No'] },
        { id: 'int_3', label: 'Is Cat6 pulled?', options: ['Yes', 'No'] },
        { id: 'int_4', label: 'Is Access Wire pulled?', options: ['Yes', 'No'] },
        { id: 'int_5', label: 'Is intercom installed?', options: ['Yes', 'No'] }
      ]
    };

    const state = {
      activeView: 'field',
      recipientEmail: DEFAULT_RECIPIENT_EMAIL,
      autoTime: '',
      reportDate: '',
      dc: '',
      techName: '',
      installType: '',
      deviceName: '',
      location: '',
      jobRef: '',
      phase: '',
      hoursWorked: '',
      blocker: 'None - On Track',
      completed: false,
      notes: '',
      answers: {},
      showValidationErrors: false,
      isOnline: typeof navigator !== 'undefined' ? Boolean(navigator.onLine) : true,
      reconnectDismissed: false,
      pmFilters: { dc: 'ALL', tech: 'ALL', status: 'ALL' },
      queue: []
    };

    const toastContainerEl = document.getElementById('toastContainer');
    const reconnectBannerEl = document.getElementById('reconnectBanner');
    const reconnectMessageEl = document.getElementById('reconnectMessage');
    const bannerOpenEmailBtnEl = document.getElementById('bannerOpenEmailBtn');
    const dismissReconnectBtnEl = document.getElementById('dismissReconnectBtn');
    const tabFieldFormBtnEl = document.getElementById('tabFieldFormBtn');
    const tabPmSummaryBtnEl = document.getElementById('tabPmSummaryBtn');
    const fieldChecklistViewEl = document.getElementById('fieldChecklistView');
    const pmSummaryViewEl = document.getElementById('pmSummaryView');
    const connectivityPillEl = document.getElementById('connectivityPill');
    const connectivityDotEl = document.getElementById('connectivityDot');
    const connectivityLabelEl = document.getElementById('connectivityLabel');
    const headerQueueBadgeBtnEl = document.getElementById('headerQueueBadgeBtn');
    const headerQueueCountEl = document.getElementById('headerQueueCount');
    const draftSaveBadgeEl = document.getElementById('draftSaveBadge');
    const recipientEmailEl = document.getElementById('recipientEmail');
    const recipientEmailErrorEl = document.getElementById('recipientEmailError');
    const liveClockBadgeEl = document.getElementById('liveClockBadge');
    const refreshTimestampBtnEl = document.getElementById('refreshTimestampBtn');
    const autoTimeDisplayEl = document.getElementById('autoTimeDisplay');
    const reportDateEl = document.getElementById('reportDate');
    const timestampMetaTextEl = document.getElementById('timestampMetaText');
    const dcSelectEl = document.getElementById('dcSelect');
    const dcErrorEl = document.getElementById('dcError');
    const techSelectEl = document.getElementById('techSelect');
    const techErrorEl = document.getElementById('techError');
    const installTypeSelectEl = document.getElementById('installTypeSelect');
    const installTypeErrorEl = document.getElementById('installTypeError');
    const deviceNameInputEl = document.getElementById('deviceNameInput');
    const locationInputEl = document.getElementById('locationInput');
    const jobRefInputEl = document.getElementById('jobRefInput');
    const phaseSelectEl = document.getElementById('phaseSelect');
    const hoursWorkedInputEl = document.getElementById('hoursWorkedInput');
    const blockerSelectEl = document.getElementById('blockerSelect');
    const deviceNameErrorEl = document.getElementById('deviceNameError');
    const locationErrorEl = document.getElementById('locationError');
    const deviceLocationFeedbackEl = document.getElementById('deviceLocationFeedback');
    const activeBranchTagEl = document.getElementById('activeBranchTag');
    const branchRequiredBadgeEl = document.getElementById('branchRequiredBadge');
    const completionTextEl = document.getElementById('completionText');
    const completionBarEl = document.getElementById('completionBar');
    const completedToggleBtnEl = document.getElementById('completedToggleBtn');
    const completedCheckBoxEl = document.getElementById('completedCheckBox');
    const emptyQuestionsStateEl = document.getElementById('emptyQuestionsState');
    const questionsContainerEl = document.getElementById('questionsContainer');
    const questionsValidationFeedbackEl = document.getElementById('questionsValidationFeedback');
    const notesInputEl = document.getElementById('notesInput');
    const previewToEl = document.getElementById('previewTo');
    const previewSubjectEl = document.getElementById('previewSubject');
    const previewBodyEl = document.getElementById('previewBody');
    const openEmailBtnEl = document.getElementById('openEmailBtn');
    const copyReportBtnEl = document.getElementById('copyReportBtn');
    const copyIconDefaultEl = document.getElementById('copyIconDefault');
    const copyIconSuccessEl = document.getElementById('copyIconSuccess');
    const copyBtnLabelEl = document.getElementById('copyBtnLabel');
    const queueOfflineReportBtnEl = document.getElementById('queueOfflineReportBtn');
    const pmFilterDcEl = document.getElementById('pmFilterDc');
    const pmFilterTechEl = document.getElementById('pmFilterTech');
    const pmFilterStatusEl = document.getElementById('pmFilterStatus');
    const pmKpiCountEl = document.getElementById('pmKpiCount');
    const pmKpiCompletedEl = document.getElementById('pmKpiCompleted');
    const pmKpiHoursEl = document.getElementById('pmKpiHours');
    const pmKpiBlockersEl = document.getElementById('pmKpiBlockers');
    const pmSummaryTableBodyEl = document.getElementById('pmSummaryTableBody');
    const offlineQueueSectionEl = document.getElementById('offlineQueueSection');
    const queueSectionBadgeCountEl = document.getElementById('queueSectionBadgeCount');
    const downloadQueueTxtBtnEl = document.getElementById('downloadQueueTxtBtn');
    const clearAllQueueBtnEl = document.getElementById('clearAllQueueBtn');
    const offlineQueueEmptyEl = document.getElementById('offlineQueueEmpty');
    const offlineQueueListEl = document.getElementById('offlineQueueList');

    function getTodayISO() {
      const now = new Date();
      const y = now.getFullYear();
      const m = String(now.getMonth() + 1).padStart(2, '0');
      const d = String(now.getDate()).padStart(2, '0');
      return `${y}-${m}-${d}`;
    }

    function formatAutoTime(dateObj = new Date()) {
      try {
        return dateObj.toLocaleString(undefined, {
          year: 'numeric', month: 'short', day: '2-digit',
          hour: '2-digit', minute: '2-digit', second: '2-digit', timeZoneName: 'short'
        });
      } catch (err) {
        return dateObj.toISOString();
      }
    }

    function formatClockTime(dateObj = new Date()) {
      try {
        return dateObj.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit', second: '2-digit' });
      } catch (err) {
        return dateObj.toTimeString().slice(0, 8);
      }
    }

    function resolveEmail(value) {
      return typeof value === 'string' ? value.trim() : '';
    }

    function isValidEmail(value) {
      const trimmed = resolveEmail(value);
      if (!trimmed) return false;
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(trimmed);
    }

    function isEffectivelyOnline() {
      return Boolean(state.isOnline);
    }

    function isValidAnswerForItem(item, value) {
      const allowed = Array.isArray(item && item.options) ? item.options : ['Yes', 'No'];
      return typeof value === 'string' && allowed.includes(value);
    }

    function parseHours(val) {
      const num = parseFloat(val);
      return Number.isFinite(num) && num > 0 ? num : 0;
    }

    function showToast(message, variant = 'info') {
      if (!toastContainerEl) return;
      const styles = {
        success: 'bg-emerald-900 text-emerald-100 border-emerald-700',
        error: 'bg-rose-900 text-rose-100 border-rose-700',
        info: 'bg-slate-900 text-slate-100 border-slate-700'
      };
      const el = document.createElement('div');
      el.className = `pointer-events-auto px-4 py-3 rounded-xl border shadow-lg text-xs sm:text-sm font-semibold transition-all duration-200 ${styles[variant] || styles.info}`;
      el.textContent = message;
      toastContainerEl.appendChild(el);
      setTimeout(() => {
        el.classList.add('opacity-0', 'translate-y-1');
        setTimeout(() => el.remove(), 220);
      }, 2800);
    }

    function safeReadStorage(key, fallback) {
      try {
        const raw = localStorage.getItem(key);
        if (!raw) return fallback;
        return JSON.parse(raw);
      } catch (err) {
        return fallback;
      }
    }

    function safeWriteStorage(key, value) {
      try {
        localStorage.setItem(key, JSON.stringify(value));
      } catch (err) {}
    }

    function copyText(text) {
      if (typeof document === 'undefined') return false;
      const textarea = document.createElement('textarea');
      textarea.value = text;
      textarea.setAttribute('readonly', '');
      textarea.style.position = 'fixed';
      textarea.style.top = '-9999px';
      textarea.style.left = '-9999px';
      document.body.appendChild(textarea);
      let copied = false;
      try {
        textarea.select();
        textarea.setSelectionRange(0, textarea.value.length);
        copied = document.execCommand('copy');
      } catch (err) {
        copied = false;
      } finally {
        document.body.removeChild(textarea);
      }
      return copied;
    }

    function setActiveView(viewName) {
      state.activeView = viewName === 'pm' ? 'pm' : 'field';
      const isPm = state.activeView === 'pm';
      fieldChecklistViewEl.classList.toggle('hidden', isPm);
      pmSummaryViewEl.classList.toggle('hidden', !isPm);
      tabFieldFormBtnEl.setAttribute('aria-selected', String(!isPm));
      tabPmSummaryBtnEl.setAttribute('aria-selected', String(isPm));
      if (isPm) {
        tabPmSummaryBtnEl.className = 'px-3 py-1 rounded-lg text-xs font-bold bg-emerald-500 text-slate-950 transition cursor-pointer';
        tabFieldFormBtnEl.className = 'px-3 py-1 rounded-lg text-xs font-bold text-slate-300 hover:text-white transition cursor-pointer';
        renderPmSummary();
      } else {
        tabFieldFormBtnEl.className = 'px-3 py-1 rounded-lg text-xs font-bold bg-emerald-500 text-slate-950 transition cursor-pointer';
        tabPmSummaryBtnEl.className = 'px-3 py-1 rounded-lg text-xs font-bold text-slate-300 hover:text-white transition cursor-pointer';
      }
    }

    function refreshAutoTime(sourceLabel = 'Refreshed', notify = false, persist = true) {
      const now = new Date();
      state.autoTime = formatAutoTime(now);
      if (autoTimeDisplayEl) autoTimeDisplayEl.value = state.autoTime;
      if (timestampMetaTextEl) timestampMetaTextEl.textContent = `Auto Time (${sourceLabel}) updated at ${formatClockTime(now)}.`;
      if (persist) saveDraft();
      updateReportPreview();
      if (notify) showToast(`Auto Time refreshed: ${state.autoTime}`, 'info');
    }

    let liveClockIntervalId = null;
    function startLiveClock() {
      const updateClock = () => {
        if (liveClockBadgeEl) {
          liveClockBadgeEl.textContent = `Clock: ${formatClockTime(new Date())}`;
        }
      };
      updateClock();
      if (liveClockIntervalId) clearInterval(liveClockIntervalId);
      liveClockIntervalId = setInterval(updateClock, 1000);
    }

    function saveDraft() {
      const emailValue = resolveEmail(state.recipientEmail);
      try { localStorage.setItem(STORAGE_KEY_EMAIL, emailValue); } catch (err) {}
      const draftPayload = {
        recipientEmail: emailValue,
        autoTime: state.autoTime || '',
        reportDate: state.reportDate || getTodayISO(),
        dc: state.dc || '',
        techName: state.techName || '',
        installType: state.installType || '',
        deviceName: state.deviceName || '',
        location: state.location || '',
        jobRef: state.jobRef || '',
        phase: state.phase || '',
        hoursWorked: state.hoursWorked || '',
        blocker: state.blocker || 'None - On Track',
        completed: Boolean(state.completed),
        notes: state.notes || '',
        answers: state.answers || {}
      };
      safeWriteStorage(STORAGE_KEY_DRAFT, draftPayload);
      if (draftSaveBadgeEl) draftSaveBadgeEl.textContent = 'Draft saved in localStorage';
    }

    function loadDraft() {
      let persistedEmail = '';
      try { persistedEmail = localStorage.getItem(STORAGE_KEY_EMAIL) || ''; } catch (err) { persistedEmail = ''; }
      const draft = safeReadStorage(STORAGE_KEY_DRAFT, null) || safeReadStorage('lead_tech_checklist_draft_v1', null);
      const effectiveEmail = resolveEmail((draft && draft.recipientEmail) || persistedEmail || DEFAULT_RECIPIENT_EMAIL);
      state.recipientEmail = effectiveEmail;
      if (recipientEmailEl) recipientEmailEl.value = effectiveEmail;
      if (!draft || typeof draft !== 'object') return;
      if (typeof draft.reportDate === 'string' && draft.reportDate) {
        state.reportDate = draft.reportDate;
        if (reportDateEl) reportDateEl.value = draft.reportDate;
      }
      if (typeof draft.autoTime === 'string' && draft.autoTime) {
        state.autoTime = draft.autoTime;
        if (autoTimeDisplayEl) autoTimeDisplayEl.value = draft.autoTime;
        if (timestampMetaTextEl) timestampMetaTextEl.textContent = 'Restored Auto Time from saved draft.';
      }
      if (typeof draft.dc === 'string' && draft.dc) {
        state.dc = draft.dc;
        if (dcSelectEl) dcSelectEl.value = draft.dc;
      }
      if (typeof draft.techName === 'string' && draft.techName) {
        state.techName = draft.techName;
        if (techSelectEl) techSelectEl.value = draft.techName;
      }
      if (typeof draft.deviceName === 'string') {
        state.deviceName = draft.deviceName;
        if (deviceNameInputEl) deviceNameInputEl.value = draft.deviceName;
      }
      if (typeof draft.location === 'string') {
        state.location = draft.location;
        if (locationInputEl) locationInputEl.value = draft.location;
      }
      if (typeof draft.jobRef === 'string') {
        state.jobRef = draft.jobRef;
        if (jobRefInputEl) jobRefInputEl.value = draft.jobRef;
      }
      if (typeof draft.phase === 'string') {
        state.phase = draft.phase;
        if (phaseSelectEl) phaseSelectEl.value = draft.phase;
      }
      if (typeof draft.hoursWorked === 'string' || typeof draft.hoursWorked === 'number') {
        state.hoursWorked = String(draft.hoursWorked);
        if (hoursWorkedInputEl) hoursWorkedInputEl.value = state.hoursWorked;
      }
      if (typeof draft.blocker === 'string' && draft.blocker) {
        state.blocker = draft.blocker;
        if (blockerSelectEl) blockerSelectEl.value = draft.blocker;
      }
      if (typeof draft.notes === 'string') {
        state.notes = draft.notes;
        if (notesInputEl) notesInputEl.value = draft.notes;
      }
      state.completed = Boolean(draft.completed);
      if (typeof draft.installType === 'string' && CHECKLIST_QUESTIONS[draft.installType]) {
        state.installType = draft.installType;
        if (installTypeSelectEl) installTypeSelectEl.value = draft.installType;
        const branchItems = CHECKLIST_QUESTIONS[draft.installType];
        const restoredAnswers = {};
        branchItems.forEach((item) => {
          const ans = draft.answers && draft.answers[item.id];
          restoredAnswers[item.id] = isValidAnswerForItem(item, ans) ? ans : null;
        });
        state.answers = restoredAnswers;
      }
    }

    function loadQueue() {
      const savedQueue = safeReadStorage(STORAGE_KEY_QUEUE, null);
      if (Array.isArray(savedQueue)) {
        state.queue = savedQueue;
      } else {
        const legacyQueue = safeReadStorage('lead_tech_checklist_queue_v1', []);
        state.queue = Array.isArray(legacyQueue) ? legacyQueue : [];
      }
    }

    function saveQueue() {
      safeWriteStorage(STORAGE_KEY_QUEUE, state.queue);
      renderQueue();
      renderPmSummary();
      syncReconnectBanner();
    }

    function syncReconnectBanner() {
      const online = isEffectivelyOnline();
      const pending = state.queue.length;
      if (online && pending > 0 && !state.reconnectDismissed) {
        reconnectMessageEl.textContent = `Connection restored. ${pending} queued report${pending === 1 ? '' : 's'} ready.`;
        reconnectBannerEl.classList.remove('hidden');
      } else {
        reconnectBannerEl.classList.add('hidden');
      }
    }

    function syncConnectivityUI(justReconnected = false) {
      const online = isEffectivelyOnline();
      if (online) {
        connectivityPillEl.className = 'inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-bold border transition bg-emerald-950/80 text-emerald-300 border-emerald-700/70';
        connectivityDotEl.className = 'w-2 h-2 rounded-full bg-emerald-400';
        connectivityLabelEl.textContent = 'Online';
      } else {
        connectivityPillEl.className = 'inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-bold border transition bg-amber-950/90 text-amber-300 border-amber-500/70';
        connectivityDotEl.className = 'w-2 h-2 rounded-full bg-amber-400 animate-pulse';
        connectivityLabelEl.textContent = 'Offline';
      }
      if (justReconnected) state.reconnectDismissed = false;
      syncReconnectBanner();
    }

    function handleConnectivityChange(onlineState) {
      const wasOnline = isEffectivelyOnline();
      state.isOnline = Boolean(onlineState);
      const nowOnline = isEffectivelyOnline();
      const justReconnected = !wasOnline && nowOnline;
      syncConnectivityUI(justReconnected);
      if (justReconnected) showToast('Back online. Connection restored.', 'success');
      else if (wasOnline && !nowOnline) showToast('Offline. Use Queue / Save Offline Report to store reports locally.', 'info');
    }

    function getCompletionMetrics() {
      const items = CHECKLIST_QUESTIONS[state.installType] || [];
      const total = items.length;
      if (total === 0) return { yesCount: 0, answeredCount: 0, total: 0, percentage: 0 };
      let yesCount = 0;
      let answeredCount = 0;
      items.forEach((item) => {
        const val = state.answers[item.id];
        if (isValidAnswerForItem(item, val)) answeredCount += 1;
        if (val === 'Yes') yesCount += 1;
      });
      const percentage = Math.round((yesCount / total) * 100);
      return { yesCount, answeredCount, total, percentage };
    }

    function getUnansweredQuestions() {
      if (!state.installType) return [];
      const items = CHECKLIST_QUESTIONS[state.installType] || [];
      return items.filter((item) => !isValidAnswerForItem(item, state.answers[item.id]));
    }

    function renderCompletedToggle() {
      if (state.completed) {
        completedToggleBtnEl.setAttribute('aria-pressed', 'true');
        completedToggleBtnEl.className = 'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold border transition cursor-pointer bg-emerald-600 text-white border-emerald-700 shadow-2xs';
        completedCheckBoxEl.className = 'w-4 h-4 rounded border border-white flex items-center justify-center text-[11px] leading-none bg-emerald-700 text-white';
      } else {
        completedToggleBtnEl.setAttribute('aria-pressed', 'false');
        completedToggleBtnEl.className = 'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold border transition cursor-pointer bg-white text-slate-700 border-slate-300 hover:bg-slate-100';
        completedCheckBoxEl.className = 'w-4 h-4 rounded border border-slate-400 flex items-center justify-center text-[11px] leading-none bg-white text-transparent';
      }
    }

    function getOptionButtonStyle(option, isSelected) {
      if (!isSelected) {
        if (option === 'Yes') return 'bg-white text-slate-700 border-slate-300 hover:bg-emerald-50 hover:border-emerald-300';
        if (option === 'No') return 'bg-white text-slate-700 border-slate-300 hover:bg-rose-50 hover:border-rose-300';
        return 'bg-white text-slate-700 border-slate-300 hover:bg-amber-50 hover:border-amber-300';
      }
      if (option === 'Yes') return 'bg-emerald-600 text-white border-emerald-700 shadow-2xs';
      if (option === 'No') return 'bg-rose-600 text-white border-rose-700 shadow-2xs';
      return 'bg-amber-600 text-white border-amber-700 shadow-2xs';
    }

    function formatChoiceList(options) {
      if (options.length === 1) return options[0];
      if (options.length === 2) return `${options[0]} or ${options[1]}`;
      return `${options.slice(0, -1).join(', ')}, or ${options[options.length - 1]}`;
    }

    function renderQuestions() {
      const items = CHECKLIST_QUESTIONS[state.installType] || [];
      if (!state.installType || items.length === 0) {
        activeBranchTagEl.classList.add('hidden');
        activeBranchTagEl.textContent = '';
        branchRequiredBadgeEl.classList.add('hidden');
        emptyQuestionsStateEl.classList.remove('hidden');
        questionsContainerEl.classList.add('hidden');
        questionsContainerEl.innerHTML = '';
        questionsValidationFeedbackEl.classList.add('hidden');
        return;
      }
      activeBranchTagEl.textContent = state.installType;
      activeBranchTagEl.classList.remove('hidden');
      branchRequiredBadgeEl.classList.remove('hidden');
      emptyQuestionsStateEl.classList.add('hidden');
      questionsContainerEl.classList.remove('hidden');
      questionsContainerEl.innerHTML = '';

      items.forEach((item, idx) => {
        const options = Array.isArray(item.options) && item.options.length > 0 ? item.options : ['Yes', 'No'];
        const selected = isValidAnswerForItem(item, state.answers[item.id]) ? state.answers[item.id] : null;
        const isUnansweredRequired = state.showValidationErrors && !selected;
        const row = document.createElement('div');
        row.setAttribute('data-question-id', item.id);
        row.className = `flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-3.5 rounded-xl border transition ${
          isUnansweredRequired
            ? 'bg-rose-50/70 border-rose-400 ring-2 ring-rose-200'
            : selected === 'Yes'
            ? 'bg-emerald-50/50 border-emerald-200'
            : selected === 'No'
            ? 'bg-rose-50/50 border-rose-200'
            : selected === 'N/A'
            ? 'bg-amber-50/50 border-amber-200'
            : 'bg-slate-50/70 border-slate-200/90'
        }`;
        const left = document.createElement('div');
        left.className = 'flex flex-wrap items-center gap-2 pr-2';
        const indexBadge = document.createElement('span');
        indexBadge.className = 'w-5 h-5 rounded-md bg-white border border-slate-300 text-[11px] font-bold text-slate-600 flex items-center justify-center shrink-0 tabular-nums';
        indexBadge.textContent = String(idx + 1);
        const questionLabel = document.createElement('span');
        questionLabel.className = 'text-sm font-medium text-slate-800';
        questionLabel.textContent = item.label;
        const reqTag = document.createElement('span');
        reqTag.className = 'text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded bg-rose-100 text-rose-700 border border-rose-200';
        reqTag.textContent = 'Required';
        left.appendChild(indexBadge);
        left.appendChild(questionLabel);
        left.appendChild(reqTag);
        if (isUnansweredRequired) {
          const missingHint = document.createElement('span');
          missingHint.className = 'w-full sm:w-auto text-xs font-semibold text-rose-700';
          missingHint.textContent = `Select ${formatChoiceList(options)}.`;
          left.appendChild(missingHint);
        }
        const btnGroup = document.createElement('div');
        btnGroup.className = 'flex flex-wrap items-center gap-2 shrink-0 self-end sm:self-center';
        options.forEach((opt) => {
          const isSelected = selected === opt;
          const optBtn = document.createElement('button');
          optBtn.type = 'button';
          optBtn.textContent = opt;
          optBtn.setAttribute('aria-pressed', String(isSelected));
          optBtn.setAttribute('aria-required', 'true');
          optBtn.className = `px-3.5 py-1.5 rounded-lg text-xs font-extrabold border transition cursor-pointer ${getOptionButtonStyle(opt, isSelected)}`;
          optBtn.addEventListener('click', () => {
            state.answers[item.id] = state.answers[item.id] === opt ? null : opt;
            saveDraft();
            renderQuestions();
            syncValidationFeedback(state.showValidationErrors);
            updateCompletionAndPreview();
          });
          btnGroup.appendChild(optBtn);
        });
        row.appendChild(left);
        row.appendChild(btnGroup);
        questionsContainerEl.appendChild(row);
      });
    }

    function updateCompletionAndPreview() {
      const { yesCount, total, percentage } = getCompletionMetrics();
      completionTextEl.textContent = `${percentage}% (${yesCount}/${total} Yes)`;
      completionBarEl.style.width = `${percentage}%`;
      renderCompletedToggle();
      updateReportPreview();
    }

    function syncValidationFeedback(showErrors = false) {
      const emailValid = isValidEmail(state.recipientEmail);
      const dcMissing = !state.dc;
      const techMissing = !state.techName;
      const installTypeMissing = !state.installType;
      const deviceMissing = !(state.deviceName || '').trim();
      const locationMissing = !(state.location || '').trim();
      const unansweredQuestions = getUnansweredQuestions();
      const errorClasses = ['border-rose-500', 'ring-2', 'ring-rose-200'];

      if (showErrors && !emailValid) {
        recipientEmailEl.classList.add(...errorClasses);
        recipientEmailErrorEl.textContent = resolveEmail(state.recipientEmail)
          ? 'Please enter a valid recipient email address (for example, name@company.com).'
          : 'Recipient Email is required before emailing, copying, or queueing a report.';
        recipientEmailErrorEl.classList.remove('hidden');
      } else if (emailValid) {
        recipientEmailEl.classList.remove(...errorClasses);
        recipientEmailErrorEl.classList.add('hidden');
      }
      if (showErrors && dcMissing) {
        dcSelectEl.classList.add(...errorClasses);
        dcErrorEl.classList.remove('hidden');
      } else if (!dcMissing) {
        dcSelectEl.classList.remove(...errorClasses);
        dcErrorEl.classList.add('hidden');
      }
      if (showErrors && techMissing) {
        techSelectEl.classList.add(...errorClasses);
        techErrorEl.classList.remove('hidden');
      } else if (!techMissing) {
        techSelectEl.classList.remove(...errorClasses);
        techErrorEl.classList.add('hidden');
      }
      if (showErrors && installTypeMissing) {
        installTypeSelectEl.classList.add('border-rose-500', 'ring-2', 'ring-rose-400');
        installTypeErrorEl.classList.remove('hidden');
      } else if (!installTypeMissing) {
        installTypeSelectEl.classList.remove('border-rose-500', 'ring-2', 'ring-rose-400');
        installTypeErrorEl.classList.add('hidden');
      }
      if (showErrors && deviceMissing) {
        deviceNameInputEl.classList.add(...errorClasses);
        deviceNameErrorEl.classList.remove('hidden');
      } else if (!deviceMissing) {
        deviceNameInputEl.classList.remove(...errorClasses);
        deviceNameErrorEl.classList.add('hidden');
      }
      if (showErrors && locationMissing) {
        locationInputEl.classList.add(...errorClasses);
        locationErrorEl.classList.remove('hidden');
      } else if (!locationMissing) {
        locationInputEl.classList.remove(...errorClasses);
        locationErrorEl.classList.add('hidden');
      }
      if (showErrors && (deviceMissing || locationMissing)) {
        const missingDevLoc = [];
        if (deviceMissing) missingDevLoc.push('Device Name');
        if (locationMissing) missingDevLoc.push('Location');
        deviceLocationFeedbackEl.textContent = `Required field missing: please enter ${missingDevLoc.join(' and ')} in Device & Location.`;
        deviceLocationFeedbackEl.classList.remove('hidden');
      } else if (!deviceMissing && !locationMissing) {
        deviceLocationFeedbackEl.classList.add('hidden');
      }
      if (showErrors && state.installType && unansweredQuestions.length > 0) {
        const names = unansweredQuestions.map((q) => q.label).join(' ');
        questionsValidationFeedbackEl.textContent = `All required ${state.installType} checklist items must be answered. Please answer: ${names}`;
        questionsValidationFeedbackEl.classList.remove('hidden');
      } else {
        questionsValidationFeedbackEl.classList.add('hidden');
      }
    }

    function validateBeforeAction() {
      state.showValidationErrors = true;
      renderQuestions();
      syncValidationFeedback(true);
      const missing = [];
      let firstInvalid = null;
      if (!isValidEmail(state.recipientEmail)) {
        missing.push(resolveEmail(state.recipientEmail) ? 'Valid Recipient Email' : 'Recipient Email');
        if (!firstInvalid) firstInvalid = recipientEmailEl;
      }
      if (!state.dc) {
        missing.push('DC Selector');
        if (!firstInvalid) firstInvalid = dcSelectEl;
      }
      if (!state.techName) {
        missing.push('Tech Name');
        if (!firstInvalid) firstInvalid = techSelectEl;
      }
      if (!state.installType) {
        missing.push('Installation Type');
        if (!firstInvalid) firstInvalid = installTypeSelectEl;
      }
      if (!(state.deviceName || '').trim()) {
        missing.push('Device Name');
        if (!firstInvalid) firstInvalid = deviceNameInputEl;
      }
      if (!(state.location || '').trim()) {
        missing.push('Location');
        if (!firstInvalid) firstInvalid = locationInputEl;
      }
      const unansweredQuestions = getUnansweredQuestions();
      if (state.installType && unansweredQuestions.length > 0) {
        missing.push(`${state.installType} checklist (${unansweredQuestions.length} unanswered)`);
        if (!firstInvalid) {
          const firstRow = questionsContainerEl.querySelector(`[data-question-id="${unansweredQuestions[0].id}"]`);
          firstInvalid = firstRow || questionsContainerEl;
        }
      }
      if (missing.length > 0) {
        showToast(`Required fields missing: ${missing.join(', ')}.`, 'error');
        if (firstInvalid && typeof firstInvalid.scrollIntoView === 'function') {
          firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
          if (typeof firstInvalid.focus === 'function') firstInvalid.focus();
        }
        return false;
      }
      state.showValidationErrors = false;
      renderQuestions();
      syncValidationFeedback(false);
      return true;
    }

    function buildReport() {
      const to = resolveEmail(state.recipientEmail) || '[Required]';
      const dc = state.dc || '[Not Selected]';
      const techName = state.techName || '[Not Selected]';
      const installType = state.installType || '[Not Selected]';
      const deviceName = (state.deviceName || '').trim() || '[Required]';
      const location = (state.location || '').trim() || '[Required]';
      const jobRef = (state.jobRef || '').trim();
      const phase = state.phase || '';
      const hoursVal = parseHours(state.hoursWorked);
      const blocker = state.blocker || 'None - On Track';
      const completedStatus = state.completed ? 'Yes' : 'No';
      const autoTime = state.autoTime || formatAutoTime(new Date());
      const reportDate = state.reportDate || getTodayISO();
      const notes = (state.notes || '').trim();
      const { yesCount, total, percentage } = getCompletionMetrics();
      const items = CHECKLIST_QUESTIONS[state.installType] || [];

      const subjectParts = [
        '[Lead Tech Daily Field Checklist]',
        dc,
        installType,
        (state.deviceName || '').trim() || 'Device',
        (state.location || '').trim() || 'Location'
      ];
      if (jobRef) subjectParts.push(jobRef);
      subjectParts.push(state.completed ? 'Completed' : 'Not Completed');
      subjectParts.push(techName);
      const subject = subjectParts.join(' - ');

      const lines = [
        'LEAD TECH DAILY FIELD CHECKLIST',
        '========================================',
        `Recipient Email:   ${to}`,
        `Report Date:       ${reportDate}`,
        `Auto Time:         ${autoTime}`,
        `DC Selector:       ${dc}`,
        `Tech Name:         ${techName}`,
        `Installation Type: ${installType}`,
        `Device Name:       ${deviceName}`,
        `Location:          ${location}`
      ];
      if (jobRef) lines.push(`Job / WO #:        ${jobRef}`);
      if (phase) lines.push(`Install Phase:     ${phase}`);
      if (hoursVal > 0) lines.push(`Hours Today:       ${hoursVal.toFixed(2)}`);
      lines.push(`Blocker Status:    ${blocker}`);
      lines.push(`Completed:         ${completedStatus}`);
      if (total > 0) lines.push(`Checklist Score:   ${percentage}% (${yesCount}/${total} Yes)`);
      lines.push('');
      lines.push('CHECKLIST:');
      lines.push('----------------------------------------');
      if (items.length === 0) {
        lines.push('(No Installation Type selected.)');
      } else {
        items.forEach((item) => {
          const val = isValidAnswerForItem(item, state.answers[item.id]) ? state.answers[item.id] : 'Unanswered';
          lines.push(`${item.label} ${val}`);
        });
      }
      lines.push('');
      lines.push('NOTES:');
      lines.push('----------------------------------------');
      lines.push(notes || '(None)');
      lines.push('========================================');

      return { to, subject, body: lines.join('\\n') };
    }

    function updateReportPreview() {
      const report = buildReport();
      if (previewToEl) previewToEl.textContent = report.to;
      if (previewSubjectEl) previewSubjectEl.textContent = report.subject;
      if (previewBodyEl) previewBodyEl.textContent = report.body;
    }

    function openMailto(toAddr, subject, body) {
      const encodedTo = encodeURIComponent(resolveEmail(toAddr));
      const encodedSubject = encodeURIComponent(subject || '');
      const encodedBody = encodeURIComponent(body || '');
      window.location.href = `mailto:${encodedTo}?subject=${encodedSubject}&body=${encodedBody}`;
    }

    function addReportToQueue(silent = false) {
      refreshAutoTime('Queued', false, true);
      const report = buildReport();
      const record = {
        id: `q_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`,
        autoTime: state.autoTime,
        reportDate: state.reportDate || getTodayISO(),
        dc: state.dc,
        techName: state.techName,
        installType: state.installType,
        deviceName: (state.deviceName || '').trim(),
        location: (state.location || '').trim(),
        jobRef: (state.jobRef || '').trim(),
        phase: state.phase || '',
        hoursWorked: parseHours(state.hoursWorked),
        blocker: state.blocker || 'None - On Track',
        completed: Boolean(state.completed),
        to: resolveEmail(state.recipientEmail),
        subject: report.subject,
        body: report.body
      };
      state.queue.unshift(record);
      saveQueue();
      if (!silent) showToast(`Queued offline report for ${record.deviceName} (${record.dc}).`, 'success');
      return record;
    }

    function handleOpenEmail() {
      if (!validateBeforeAction()) return;
      if (!isEffectivelyOnline()) {
        addReportToQueue(true);
        showToast('Offline. No active connection detected; report saved to Offline Report Queue.', 'info');
        return;
      }
      refreshAutoTime('Email', false, true);
      const report = buildReport();
      try {
        openMailto(report.to, report.subject, report.body);
        showToast(`Opening email to ${report.to}...`, 'success');
      } catch (err) {
        addReportToQueue(true);
        showToast('Could not open mail client. Report saved to Offline Report Queue.', 'info');
      }
    }

    function handleCopyReport() {
      if (!validateBeforeAction()) return;
      refreshAutoTime('Copied', false, true);
      const report = buildReport();
      const fullPayload = `To: ${report.to}\\nSubject: ${report.subject}\\n\\n${report.body}`;
      if (copyText(fullPayload)) {
        copyBtnLabelEl.textContent = 'Copied!';
        copyIconDefaultEl.classList.add('hidden');
        copyIconSuccessEl.classList.remove('hidden');
        showToast('Report copied to clipboard.', 'success');
        setTimeout(() => {
          copyBtnLabelEl.textContent = 'Copy Report';
          copyIconDefaultEl.classList.remove('hidden');
          copyIconSuccessEl.classList.add('hidden');
        }, 2000);
      } else {
        showToast('Could not copy report to clipboard.', 'error');
      }
    }

    function handleQueueOfflineReport() {
      if (!validateBeforeAction()) return;
      addReportToQueue(false);
    }

    function getFilteredQueue() {
      return state.queue.filter((entry) => {
        if (state.pmFilters.dc !== 'ALL' && entry.dc !== state.pmFilters.dc) return false;
        if (state.pmFilters.tech !== 'ALL' && entry.techName !== state.pmFilters.tech) return false;
        const isBlocked = entry.blocker && entry.blocker !== 'None - On Track';
        if (state.pmFilters.status === 'COMPLETED' && !entry.completed) return false;
        if (state.pmFilters.status === 'INCOMPLETE' && entry.completed) return false;
        if (state.pmFilters.status === 'BLOCKED' && !isBlocked) return false;
        return true;
      });
    }

    function renderPmSummary() {
      if (!pmSummaryTableBodyEl) return;
      const filtered = getFilteredQueue();
      const totalHours = filtered.reduce((acc, item) => acc + parseHours(item.hoursWorked), 0);
      const completedCount = filtered.filter((item) => Boolean(item.completed)).length;
      const blockedCount = filtered.filter((item) => item.blocker && item.blocker !== 'None - On Track').length;
      if (pmKpiCountEl) pmKpiCountEl.textContent = String(filtered.length);
      if (pmKpiCompletedEl) pmKpiCompletedEl.textContent = String(completedCount);
      if (pmKpiHoursEl) pmKpiHoursEl.textContent = totalHours.toFixed(1);
      if (pmKpiBlockersEl) pmKpiBlockersEl.textContent = String(blockedCount);
      pmSummaryTableBodyEl.innerHTML = '';
      if (filtered.length === 0) {
        const tr = document.createElement('tr');
        const td = document.createElement('td');
        td.colSpan = 6;
        td.className = 'px-4 py-6 text-center text-slate-500';
        td.textContent = state.queue.length === 0
          ? 'No queued reports yet. Queue reports in the Field Checklist tab to build a multi-day PM summary.'
          : 'No queued reports match the active PM filters.';
        tr.appendChild(td);
        pmSummaryTableBodyEl.appendChild(tr);
        return;
      }
      filtered.forEach((entry) => {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-50';
        const dcTd = document.createElement('td');
        dcTd.className = 'px-3.5 py-2.5 font-semibold text-slate-900 whitespace-nowrap';
        dcTd.textContent = entry.dc || '-';
        const devTd = document.createElement('td');
        devTd.className = 'px-3.5 py-2.5 text-slate-800';
        devTd.textContent = entry.jobRef ? `${entry.deviceName || '-'} (${entry.jobRef})` : (entry.deviceName || '-');
        const phaseTd = document.createElement('td');
        phaseTd.className = 'px-3.5 py-2.5 text-slate-600';
        phaseTd.textContent = entry.phase || entry.installType || '-';
        const techTd = document.createElement('td');
        techTd.className = 'px-3.5 py-2.5 font-medium text-slate-800 whitespace-nowrap';
        techTd.textContent = entry.techName || '-';
        const hrsTd = document.createElement('td');
        hrsTd.className = 'px-3.5 py-2.5 font-mono font-semibold text-slate-900 tabular-nums whitespace-nowrap';
        hrsTd.textContent = parseHours(entry.hoursWorked).toFixed(2);
        const blockerTd = document.createElement('td');
        blockerTd.className = 'px-3.5 py-2.5 whitespace-nowrap';
        const isBlocked = entry.blocker && entry.blocker !== 'None - On Track';
        const badge = document.createElement('span');
        badge.className = isBlocked
          ? 'px-2 py-0.5 rounded-md bg-amber-100 text-amber-900 border border-amber-200 text-xs font-bold'
          : entry.completed
          ? 'px-2 py-0.5 rounded-md bg-emerald-100 text-emerald-900 border border-emerald-200 text-xs font-bold'
          : 'px-2 py-0.5 rounded-md bg-slate-100 text-slate-700 border border-slate-200 text-xs font-semibold';
        badge.textContent = isBlocked ? entry.blocker : (entry.completed ? 'Completed' : 'In Progress');
        blockerTd.appendChild(badge);
        tr.appendChild(dcTd);
        tr.appendChild(devTd);
        tr.appendChild(phaseTd);
        tr.appendChild(techTd);
        tr.appendChild(hrsTd);
        tr.appendChild(blockerTd);
        pmSummaryTableBodyEl.appendChild(tr);
      });
    }

    function queueCopyItem(id) {
      const entry = state.queue.find((item) => item.id === id);
      if (!entry) return;
      const toAddr = resolveEmail(entry.to) || '[Required]';
      const text = `To: ${toAddr}\\nSubject: ${entry.subject}\\n\\n${entry.body}`;
      if (copyText(text)) showToast(`Copied queued report (${entry.deviceName}).`, 'success');
      else showToast('Failed to copy queued report.', 'error');
    }

    function queueOpenEmailItem(id) {
      const entry = state.queue.find((item) => item.id === id);
      if (!entry) return;
      if (!isValidEmail(entry.to)) {
        showToast('Queued report is missing a valid recipient email address.', 'error');
        return;
      }
      if (!isEffectivelyOnline()) {
        showToast('Offline. Reconnect to open email.', 'error');
        return;
      }
      openMailto(entry.to, entry.subject, entry.body);
      showToast(`Opening email for ${entry.deviceName}...`, 'success');
    }

    function queueDeleteItem(id) {
      state.queue = state.queue.filter((item) => item.id !== id);
      saveQueue();
      showToast('Deleted report from Offline Report Queue.', 'info');
    }

    function handleDownloadQueueTxt() {
      if (state.queue.length === 0) return;
      const content = state.queue
        .map((entry, idx) => [
          '====================================================================',
          `REPORT #${idx + 1} | Auto Time: ${entry.autoTime}`,
          `To:      ${resolveEmail(entry.to) || '[Required]'}`,
          `Subject: ${entry.subject}`,
          '====================================================================',
          entry.body,
          ''
        ].join('\\n'))
        .join('\\n');
      const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `Lead_Tech_Offline_Queue_${getTodayISO()}.txt`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      showToast(`Downloaded ${state.queue.length} queued report(s) as .txt.`, 'success');
    }

    function handleClearAllQueue() {
      if (state.queue.length === 0) return;
      state.queue = [];
      saveQueue();
      showToast('Cleared all reports from Offline Report Queue.', 'info');
    }

    function renderQueue() {
      const count = state.queue.length;
      if (headerQueueCountEl) headerQueueCountEl.textContent = String(count);
      if (queueSectionBadgeCountEl) queueSectionBadgeCountEl.textContent = String(count);
      if (downloadQueueTxtBtnEl) downloadQueueTxtBtnEl.disabled = count === 0;
      if (clearAllQueueBtnEl) clearAllQueueBtnEl.disabled = count === 0;
      if (count === 0) {
        if (offlineQueueEmptyEl) offlineQueueEmptyEl.classList.remove('hidden');
        if (offlineQueueListEl) {
          offlineQueueListEl.classList.add('hidden');
          offlineQueueListEl.innerHTML = '';
        }
        return;
      }
      if (offlineQueueEmptyEl) offlineQueueEmptyEl.classList.add('hidden');
      if (offlineQueueListEl) {
        offlineQueueListEl.classList.remove('hidden');
        offlineQueueListEl.innerHTML = '';
      }
      state.queue.forEach((entry) => {
        const card = document.createElement('div');
        card.className = 'rounded-xl border border-slate-200 bg-slate-50/70 p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3';
        const info = document.createElement('div');
        info.className = 'space-y-1 min-w-0';
        const badges = document.createElement('div');
        badges.className = 'flex flex-wrap items-center gap-1.5';
        const dcBadge = document.createElement('span');
        dcBadge.className = 'px-2 py-0.5 rounded-md bg-slate-900 text-emerald-300 text-xs font-bold';
        dcBadge.textContent = entry.dc || '-';
        const typeBadge = document.createElement('span');
        typeBadge.className = 'text-xs sm:text-sm font-bold text-slate-900';
        typeBadge.textContent = entry.installType || '-';
        const devBadge = document.createElement('span');
        devBadge.className = 'px-2 py-0.5 rounded-md bg-white border border-slate-300 text-xs font-bold text-slate-800';
        devBadge.textContent = `Device: ${entry.deviceName || '-'}`;
        const locBadge = document.createElement('span');
        locBadge.className = 'px-2 py-0.5 rounded-md bg-white border border-slate-200 text-xs font-semibold text-slate-600';
        locBadge.textContent = `Location: ${entry.location || '-'}`;
        const doneBadge = document.createElement('span');
        doneBadge.className = entry.completed
          ? 'px-2 py-0.5 rounded-md bg-emerald-100 text-emerald-800 border border-emerald-200 text-xs font-bold'
          : 'px-2 py-0.5 rounded-md bg-amber-100 text-amber-800 border border-amber-200 text-xs font-bold';
        doneBadge.textContent = entry.completed ? 'Completed: Yes' : 'Completed: No';
        badges.appendChild(dcBadge);
        badges.appendChild(typeBadge);
        badges.appendChild(devBadge);
        badges.appendChild(locBadge);
        badges.appendChild(doneBadge);
        if (parseHours(entry.hoursWorked) > 0) {
          const hrsBadge = document.createElement('span');
          hrsBadge.className = 'px-2 py-0.5 rounded-md bg-sky-100 text-sky-900 border border-sky-200 text-xs font-bold tabular-nums';
          hrsBadge.textContent = `${parseHours(entry.hoursWorked).toFixed(2)}h`;
          badges.appendChild(hrsBadge);
        }
        const subline = document.createElement('p');
        subline.className = 'text-[11px] font-mono text-slate-500';
        subline.textContent = `To: ${resolveEmail(entry.to) || '[Required]'} • Tech: ${entry.techName || '-'} • Auto Time: ${entry.autoTime || '-'}`;
        info.appendChild(badges);
        info.appendChild(subline);
        const actions = document.createElement('div');
        actions.className = 'flex flex-wrap items-center gap-2 shrink-0 self-end sm:self-center';
        const openEmailItemBtn = document.createElement('button');
        openEmailItemBtn.type = 'button';
        openEmailItemBtn.textContent = 'Open Email';
        openEmailItemBtn.className = 'px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold transition cursor-pointer';
        openEmailItemBtn.addEventListener('click', () => queueOpenEmailItem(entry.id));
        const copyItemBtn = document.createElement('button');
        copyItemBtn.type = 'button';
        copyItemBtn.textContent = 'Copy';
        copyItemBtn.className = 'px-3 py-1.5 rounded-lg bg-white hover:bg-slate-100 text-slate-800 border border-slate-300 text-xs font-bold transition cursor-pointer';
        copyItemBtn.addEventListener('click', () => queueCopyItem(entry.id));
        const deleteItemBtn = document.createElement('button');
        deleteItemBtn.type = 'button';
        deleteItemBtn.textContent = 'Delete';
        deleteItemBtn.className = 'px-3 py-1.5 rounded-lg bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 text-xs font-bold transition cursor-pointer';
        deleteItemBtn.addEventListener('click', () => queueDeleteItem(entry.id));
        actions.appendChild(openEmailItemBtn);
        actions.appendChild(copyItemBtn);
        actions.appendChild(deleteItemBtn);
        card.appendChild(info);
        card.appendChild(actions);
        if (offlineQueueListEl) offlineQueueListEl.appendChild(card);
      });
    }

    let eventsBound = false;
    function bindEvents() {
      if (eventsBound) return;
      eventsBound = true;
      tabFieldFormBtnEl.addEventListener('click', () => setActiveView('field'));
      tabPmSummaryBtnEl.addEventListener('click', () => setActiveView('pm'));
      pmFilterDcEl.addEventListener('change', (e) => { state.pmFilters.dc = e.target.value; renderPmSummary(); });
      pmFilterTechEl.addEventListener('change', (e) => { state.pmFilters.tech = e.target.value; renderPmSummary(); });
      pmFilterStatusEl.addEventListener('change', (e) => { state.pmFilters.status = e.target.value; renderPmSummary(); });
      recipientEmailEl.addEventListener('input', (e) => {
        state.recipientEmail = resolveEmail(e.target.value);
        syncValidationFeedback(state.showValidationErrors);
        saveDraft();
        updateReportPreview();
      });
      recipientEmailEl.addEventListener('blur', () => {
        if (!isValidEmail(state.recipientEmail)) {
          recipientEmailErrorEl.textContent = resolveEmail(state.recipientEmail)
            ? 'Please enter a valid recipient email address (for example, name@company.com).'
            : 'Recipient Email is required before emailing, copying, or queueing a report.';
          recipientEmailErrorEl.classList.remove('hidden');
          recipientEmailEl.classList.add('border-rose-500', 'ring-2', 'ring-rose-200');
        }
      });
      refreshTimestampBtnEl.addEventListener('click', () => refreshAutoTime('Manual Refresh', true, true));
      reportDateEl.addEventListener('change', (e) => { state.reportDate = e.target.value || getTodayISO(); saveDraft(); updateReportPreview(); });
      dcSelectEl.addEventListener('change', (e) => { state.dc = e.target.value; syncValidationFeedback(state.showValidationErrors); saveDraft(); updateReportPreview(); });
      techSelectEl.addEventListener('change', (e) => { state.techName = e.target.value; syncValidationFeedback(state.showValidationErrors); saveDraft(); updateReportPreview(); });
      installTypeSelectEl.addEventListener('change', (e) => {
        const selectedBranch = e.target.value;
        state.installType = selectedBranch;
        state.showValidationErrors = false;
        const freshAnswers = {};
        (CHECKLIST_QUESTIONS[selectedBranch] || []).forEach((item) => { freshAnswers[item.id] = null; });
        state.answers = freshAnswers;
        syncValidationFeedback(false);
        saveDraft();
        renderQuestions();
        updateCompletionAndPreview();
      });
      deviceNameInputEl.addEventListener('input', (e) => { state.deviceName = e.target.value; syncValidationFeedback(state.showValidationErrors); saveDraft(); updateReportPreview(); });
      deviceNameInputEl.addEventListener('blur', () => {
        if (!(state.deviceName || '').trim()) {
          deviceNameErrorEl.classList.remove('hidden');
          deviceNameInputEl.classList.add('border-rose-500', 'ring-2', 'ring-rose-200');
        }
      });
      locationInputEl.addEventListener('input', (e) => { state.location = e.target.value; syncValidationFeedback(state.showValidationErrors); saveDraft(); updateReportPreview(); });
      locationInputEl.addEventListener('blur', () => {
        if (!(state.location || '').trim()) {
          locationErrorEl.classList.remove('hidden');
          locationInputEl.classList.add('border-rose-500', 'ring-2', 'ring-rose-200');
        }
      });
      jobRefInputEl.addEventListener('input', (e) => { state.jobRef = e.target.value; saveDraft(); updateReportPreview(); });
      phaseSelectEl.addEventListener('change', (e) => { state.phase = e.target.value; saveDraft(); updateReportPreview(); });
      hoursWorkedInputEl.addEventListener('input', (e) => { state.hoursWorked = e.target.value; saveDraft(); updateReportPreview(); });
      blockerSelectEl.addEventListener('change', (e) => { state.blocker = e.target.value; saveDraft(); updateReportPreview(); });
      completedToggleBtnEl.addEventListener('click', () => { state.completed = !state.completed; renderCompletedToggle(); saveDraft(); updateReportPreview(); });
      notesInputEl.addEventListener('input', (e) => { state.notes = e.target.value; saveDraft(); updateReportPreview(); });
      openEmailBtnEl.addEventListener('click', handleOpenEmail);
      copyReportBtnEl.addEventListener('click', handleCopyReport);
      queueOfflineReportBtnEl.addEventListener('click', handleQueueOfflineReport);
      downloadQueueTxtBtnEl.addEventListener('click', handleDownloadQueueTxt);
      clearAllQueueBtnEl.addEventListener('click', handleClearAllQueue);
      headerQueueBadgeBtnEl.addEventListener('click', () => {
        setActiveView('field');
        offlineQueueSectionEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
      bannerOpenEmailBtnEl.addEventListener('click', () => {
        reconnectBannerEl.classList.add('hidden');
        if (state.queue.length > 0 && isEffectivelyOnline()) {
          const first = state.queue[0];
          if (!isValidEmail(first.to)) {
            showToast('Queued report is missing a valid recipient email address.', 'error');
            return;
          }
          openMailto(first.to, first.subject, first.body);
          showToast(`Opening email for queued report (${first.deviceName})...`, 'success');
        }
      });
      dismissReconnectBtnEl.addEventListener('click', () => {
        state.reconnectDismissed = true;
        reconnectBannerEl.classList.add('hidden');
      });
      window.addEventListener('online', () => handleConnectivityChange(true));
      window.addEventListener('offline', () => handleConnectivityChange(false));
    }

    function registerServiceWorker() {
      try {
        if (typeof window === 'undefined' || !('serviceWorker' in navigator)) return;
        if (!window.location || !['http:', 'https:'].includes(window.location.protocol)) return;
        navigator.serviceWorker.register('./sw.js').then((reg) => {
          if (reg && typeof reg.update === 'function') reg.update().catch(() => {});
        }).catch(() => {});
      } catch (err) {}
    }

    function init() {
      loadQueue();
      const todayISO = getTodayISO();
      state.reportDate = todayISO;
      if (reportDateEl) reportDateEl.value = todayISO;
      loadDraft();
      if (!state.reportDate) {
        state.reportDate = todayISO;
        if (reportDateEl) reportDateEl.value = todayISO;
      }
      if (!state.autoTime) refreshAutoTime('Initial Load', false, true);
      else {
        if (autoTimeDisplayEl) autoTimeDisplayEl.value = state.autoTime;
        saveDraft();
      }
      bindEvents();
      startLiveClock();
      renderQuestions();
      updateCompletionAndPreview();
      renderQueue();
      renderPmSummary();
      syncConnectivityUI(false);
      registerServiceWorker();
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
    else init();
  </script>
</body>
</html>
"""

# Ensure no literal unescaped newlines inside lines.join('...')
html = re.sub(r"\.join\('[\r\n]*'\)", r".join('\\n')", html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Wrote index.html successfully. Size:", len(html))