;;; invalid.il - Deliberately malformed input for qcover cleanup tests.

procedure(qcoverFixtureInvalid(value)
  if(value then
    'missing_close
)
