# Test sections

## Private: A

should be removed because it is in a private section

### B

should be removed because it is a child of a private section

#### C

should be removed because it is a child of a private section

## D

Should be kept because it is a peer of the removed section

### Private: E

should be removed because it is in a private section

## F

This should be kept

```markdown
## Private: G
```

### H

This should be kept, since the other value is in a listing and not a real heading.

## private: I

Lower case, but it should be removed still

## prIVaTe: J

Weird case, but it should be removed still

## PRIVATE: K

Upper case, but it should be removed still

## not private: L

should be kept, sice it does not start with `private: `

## Private:M

no space, but it should be removed

## Private:

no title, but it should be removed

## Private

no colon, so it should be kept

