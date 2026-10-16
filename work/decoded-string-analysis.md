# Concatenated decoded-string analysis

Collected from the completed Potassium workspace file `decoded_strings.log` for PID `21692`, in record order, after the VM string-builder hook.

- File size: 26,192 bytes
- Records: 2,185 newline-delimited records
- VM records with the three-byte zero prefix: 2,125
- Concatenated payload after removing that prefix: 17,209 bytes
- Printable ASCII ratio after prefix removal: 0.3809
- SHA-256 after prefix removal: `a0284efe011d85edb36cf5f0a4479108ad5c8cc1ef8ca7af469ac3c1fd3a5b5c`

## Result

The concatenated stream is not readable source. It is mostly binary/noise, with a readable tail containing runtime/library names:

`__add`, `__call`, `__concat`, `__div`, `__eq`, `__index`, `__le`, `__lt`, `__metatable`, `__mod`, `__mul`, `__newindex`, `__pow`, `__sub`, `__tostring`, `_VERSION`, `boolean`, `byte`, `char`, `concat`, `getmetatable`, `match`, `next`, `number`, `pcall`, `print`, `rawequal`, `rawget`, `rawset`, `select`, `setmetatable`, `string`, `table`, `tonumber`, `tostring`, `type`.

## Interpretation

Concatenating the values confirms that the hook is observing VM/runtime data, not the final source representation. The readable tail is the VM's standard-library/metamethod name table. The remaining step is to reconstruct the VM instruction stream and map those names to call sites; string concatenation alone does not yield the original source.
