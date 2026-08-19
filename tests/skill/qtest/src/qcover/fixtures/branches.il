;;; branches.il - Classic SKILL fixture for qcover branch instrumentation.

qcoverFixtureSideEffects = 0
qcoverFixtureQuotedExpected = '(if(t then "data" else "not code"))

procedure(qcoverFixtureIf(value)
  if(value then
    'yes
  else
    'no
  )
)

procedure(qcoverFixtureIfNoElse(value)
  if(value then
    'yes
  )
)

procedure(qcoverFixtureWhen(value)
  let((result)
    when(value
      result = 'yes
    )
    result
  )
)

procedure(qcoverFixtureUnless(value)
  let((result)
    unless(value
      result = 'yes
    )
    result
  )
)

procedure(qcoverFixtureCond(value)
  cond(
    (value == 1 'one)
    (value == 2 'two)
    (t 'other)
  )
)

procedure(qcoverFixtureNested(first second)
  if(first then
    if(second then 'both else 'first)
  else
    'none
  )
)

procedure(qcoverFixtureOnce()
  if((qcoverFixtureSideEffects = qcoverFixtureSideEffects + 1) == 1 then
    'first
  else
    'later
  )
)

procedure(qcoverFixtureQuoted()
  '(if(t then "data" else "not code"))
)
