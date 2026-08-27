# Workspace and transactions

`Workspace` is the raw bridge connection: every documented `axl*` function is
callable on it (see [Raw AXL access](../guide/raw-axl.md)), and its
`transaction` property exposes the SKILL transaction kernel directly (see
[Transactions](../guide/transactions.md)).

::: allegrobridge.Workspace
    options:
      show_bases: false
      members:
        - transaction
        - open
        - close

::: allegrobridge.client.workspace.Txn

::: allegrobridge.client.workspace.SavepointSuccess

::: allegrobridge.client.workspace.SavepointFailure
