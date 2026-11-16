# Signing key

Every package SIVACOR verifies comes with a TRO declaration and a detached
signature over it (the `.jsonld` and `.sig` files in the package's `tro`
folder). The signature is made with the key on this page.

The TRO also carries a copy of the public key (`trov:publicKey`), but that copy
cannot vouch for itself: anyone can sign a declaration with a key of their own
and embed that key. To know that a TRO was signed by SIVACOR, check its
signature against the key published here, outside the TRO.

(signing-key-fingerprint)=
## Fingerprint

The current signing key has this fingerprint:

```
F7DB 4853 9F20 7AD4 612D  C408 D8BB 2071 862A FF4A
```

It is what to compare: a key is identified by its fingerprint, not by its name
or e-mail address, which anyone can put in a key of their own.

| | |
|---|---|
| Algorithm | ed25519 (signing), cv25519 (encryption subkey) |
| Created | 2025-11-13 |
| Expires | never |
| User IDs | `SIVACOR TRS <editors@sivacor.org>`, `Admin SIVACOR <admin@sivacor.org>` |
| Status | current |

## The key

The canonical copy of the key is the file at

**<https://docs.sivacor.org/keys/sivacor-trs.asc>**

That address is stable, and is the one to use from scripts. The block below is
the same file, included into this page when the site is built, so the two
cannot differ.

```{literalinclude} ../keys/sivacor-trs.asc
```

A copy is also on the [Ubuntu key server](https://keyserver.ubuntu.com/pks/lookup?search=0xF7DB48539F207AD4612DC408D8BB2071862AFF4A&fingerprint=on&op=index).
That server accepts uploads from anyone, so it is a convenience, not a source
of trust: confirm the fingerprint against this page.

(checking-the-signature)=
## Checking a TRO's signature

`tro-utils` does not check the signature yet, so this is done with GnuPG. Use
`gpgv` with a keyring holding only the SIVACOR key, so that nothing is imported
into your own keyring and no other key can satisfy the check:

```bash
curl -fsSO https://docs.sivacor.org/keys/sivacor-trs.asc
gpg --dearmor < sivacor-trs.asc > sivacor-trs.gpg
gpgv --keyring ./sivacor-trs.gpg tro/tro-<id>.sig tro/tro-<id>.jsonld
```

The `./` matters: without it, `gpgv` looks for the keyring in its own home
directory instead. A valid signature looks like this:

```
gpgv: Signature made ...
gpgv:                using EDDSA key F7DB48539F207AD4612DC408D8BB2071862AFF4A
gpgv: Good signature from "Admin SIVACOR <admin@sivacor.org>"
gpgv:                 aka "SIVACOR TRS <editors@sivacor.org>"
```

Compare the fingerprint `gpgv` prints with the [one above](#signing-key-fingerprint).
`Good signature` means the declaration is exactly as SIVACOR signed it; any
change to it, down to a single byte, makes the check fail.

:::{warning}
Do not check the signature with the key embedded in the TRO
(`trov:publicKey`). That only shows that the declaration, its signature and the
embedded key agree with each other, which a forged TRO also achieves.
:::

The trusted timestamp (the `.tsr` file) is checked separately, with
`tro-utils verify-timestamp`; see [the FAQ](#checking-tro-files).
It proves *when* the declaration and signature existed, which is what keeps a
TRO verifiable after the key that signed it is retired.

## Key life cycle

- **Expiry.** The current key has no expiry date.
- **Replacement.** If SIVACOR changes keys, the new key is added to this page
  and the old one stays listed, with the dates it was in use, so that TROs it
  signed remain verifiable. A retired key is never removed from this page.
- **Revocation.** If a key is ever compromised, its revocation is published
  here and on the key servers, with the date it stopped being trustworthy. A
  TRO signed with it before that date stays verifiable through its trusted
  timestamp, which proves the signature already existed.

## History

What SIVACOR has written into its TROs over time. Signed TROs cannot be
changed, so an older TRO keeps whatever was current when it was made.

| Date | Change |
|---|---|
| 2025-11-13 | Key `F7DB 4853 … 862A FF4A` created, with user ID `SIVACOR TRS <editors@sivacor.org>`. |
| 2026-01-30 | User ID `Admin SIVACOR <admin@sivacor.org>` added to the same key. TROs signed after this date embed a copy of the key with both user IDs; the fingerprint is unchanged. |

The contact address that a TRO gives for SIVACOR (`trov:wasAssembledBy` /
`trov:contact`) was the placeholder `email@goes.here` in early TROs, such as one
signed on 2025-12-10. It has since been corrected to `admin@sivacor.org`, which
TROs from at least 2026-05-14 carry. Either way, the TRO was signed by the key
above, and <support@sivacor.org> is the address to write to.
