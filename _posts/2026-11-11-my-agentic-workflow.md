---
layout: post
title: "My agentic workflow"
date: 2026-11-11
tags: [ai-assisted-coding]
---

I've been writing about AI-assisted coding, but how do I actually use AI to help me code? **What is my actual workflow?**

AI or not, this is the basic lifecycle I've observed for my work:
1. **File the task** in an issue-tracker (GitLab for us)
2. **Flesh out the plan.** What exact behavior we want, core implementation choices, how to handle edge cases, etc.
3. **Code it out.** Follow the plan to actually write the changes.
4. **Verify myself.** Check functional changes - *does the new software do what I want?* - as well as non-functional - *is it well-tested, well-written?* This is often done in tandem with step 3.
5. **Get the necessary approvals.** If someone asked me for the change, confirm what landed is what they want. Get a second code-reviewer if necessary. Goes back to step 3 if changes are needed.
6. **Merge into main** when it's approved by everyone who needs to approve it, finalizing the change.

At first, AI agents would just help me with step 3 - doing the actual coding.

### But over time, it started taking on more and more of this loop.

In my case, it's Claude, with the max subscription my work generously gave me.

The foundation of this AI-powered-automated-workflow is two pieces:
1. Tracking the tasks locally in my filesystem so Claude has full access (I don't give it access to the remote issue-tracker)
2. Turning the pieces of this workflow into reusable [*skills*](https://support.claude.com/en/articles/12512176-what-are-skills) I can consistently run

### The nice thing about the first step is that Claude now has a structure to record everything about my work.

If I make a decision about a behavior direction, it's recorded.

If I say "we can't work more on this until so-and-so approves" it's recorded.

Whatever happens to a task - more work needs to be done, it's been verified by so many agent reviews, etc. - is tracked persistently (with git, so searching history and reverting comes for free).

That means **no information is lost when a session dies.** I can start up fresh, focused sessions all the time, and they know where to find and record anything.

### And whenever I noticed myself prompting the same type of thing, I usually turn it into a skill.

For the lifecycle of a task, this turned out to be:
- `/new <idea>`: file a new task, or could be multiple tasks, based on what you roughly want. Gives it priority and if it's blocked by anything so you know when to get to it.
- `/spec <task>`: flesh the task out - Claude asks questions to decide what exactly is to be done until it's as well-planned as can be
- `/ship <task>`: actually implement the plan. This can be also run in later rounds to implement requested changes.
- `/try <task>`: Claude sets up everything so I can walk through, step-by-step, the change to get a feel for it. I might also ask questions and request changes, sending back to `/ship`.
- `/publish <task>`: When I'm ready for the code changes to be up on the remote issue tracker. Since Claude can't actually push the changes itself, this skill prepares a script for me to run myself.
- `/merge <task>`: Once everyone (Claude, me, any other human reviewers) is happy with the changes, this does a final check to make sure it's good to go into main, and I still go to the issue tracker to manually merge the changes myself.
- `/closeout <task>`: After it's been merged to main and I pull the new changes, Claude takes care of marking the task as complete and updating any outstanding tasks as necessary with the new changes.

All in all, it just makes a predictable workflow for anything I'm trying to accomplish, greatly reducing the cognitive load and overhead time, so I focus on what matters.

My contributions have actually skyrocketed to **4.5 times what they used to be**!

And my days of getting deep in the weeds of the code are replaced with deep in the weeds of 5 or 6 different sessions, all working on different tasks in different stages that need me for different things.

### There's a lot more to unpack about the learned lessons I've baked into this workflow.

Automated adversarial review loops, being intentional about the human review process, how to really get the agents to do what you want, but those are subjects for future posts.

My hope is that sharing this setup can provide a common ground as I go more in depth about some of of these lessons.

Until then, stay flexible and keep learning fast!
