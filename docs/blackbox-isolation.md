# Blackbox isolation

The challenge implementation, expected flags, and scoring logic are benchmark assets and must not be mounted into the agent workspace. Expose only the target service and the task prompt. Run each target in a disposable, isolated Docker or VM network and collect evaluator output outside the target container.
