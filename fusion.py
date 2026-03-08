#!/usr/bin/env python3
import sys
import re
from collections import defaultdict


def parse_gedcom(lines):
    """Parse GEDCOM lines into a list of records. Each record is a tuple (id, type, lines)."""
    records = []
    current = None
    for line in lines:
        if line.startswith('0 '):
            if current:
                records.append(current)
            m = re.match(r"0 (@[^@]+@)\s+(\w+)", line)
            if m:
                rid, rtype = m.groups()
            else:
                # anonymous record
                rid = None
                parts = line.strip().split()
                rtype = parts[-1] if parts else None
            current = [rid, rtype, [line.rstrip('\n')]]
        else:
            if current is None:
                # stray line? include with pseudo record
                current = [None, None, [line.rstrip('\n')]]
            else:
                current[2].append(line.rstrip('\n'))
    if current:
        records.append(current)
    return records


def extract_individual_info(rec_lines):
    """Return (surname, given, birth_date) from individual record lines."""
    name = None
    birth = None
    for i, line in enumerate(rec_lines):
        parts = line.split(' ', 2)
        if len(parts) >= 3 and parts[1] == 'NAME':
            name = parts[2].strip()
        if parts[1] == 'BIRT':
            # next line may have DATE
            if i+1 < len(rec_lines):
                nextl = rec_lines[i+1].strip()
                if nextl.startswith('2 DATE'):
                    birth = nextl[len('2 DATE'):].strip()
    surname = ''
    given = ''
    if name:
        # name format: Given /Surname/
        m = re.match(r"(.*)/([^/]+)/(.*)", name)
        if m:
            given = m.group(1).strip() + (" " + m.group(3).strip() if m.group(3).strip() else "")
            surname = m.group(2).strip()
        else:
            # fallback: take last word as surname
            parts = name.split()
            if parts:
                surname = parts[-1]
                given = " ".join(parts[:-1])
    return surname, given, birth


def validate_gedcom_records(records):
    """Perform basic validation checks, return list of errors."""
    errors = []
    ids = set()
    for rid, rtype, lines in records:
        if rid:
            if rid in ids:
                errors.append(f"Duplicate record ID {rid}")
            ids.add(rid)
        # track duplicate level/tag combinations (simple GEDCOM validator style)
        seen_tags = set()
        for line in lines:
            m = re.match(r"(\d+) ", line)
            if not m:
                errors.append(f"Malformed line (no level): {line}")
                continue
            lvl = int(m.group(1))
            parts = line.split()
            tag = parts[1] if len(parts) > 1 else None
            if tag:
                key = (lvl, tag)
                if key in seen_tags:
                    errors.append(f"Duplicate occurrence of label {tag} at level {lvl} in record {rid}")
                seen_tags.add(key)
    # reference integrity
    for rid, rtype, lines in records:
        for line in lines:
            parts = line.split()
            if len(parts) >= 3:
                tag = parts[1]
                if tag in ('FAMS','FAMC','HUSB','WIFE','CHIL'):  # references
                    pid = parts[2]
                    if pid.startswith('@') and pid not in ids:
                        errors.append(f"Reference to unknown id {pid} in record {rid}")
    return errors


def main():
    if len(sys.argv) != 3:
        print("Usage: fusion.py input.ged output.ged")
        sys.exit(1)
    infile, outfile = sys.argv[1], sys.argv[2]
    with open(infile, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    records = parse_gedcom(lines)

    # separate individuals and families
    individuals = {}
    families = {}
    order = []  # preserve record order
    for rid, rtype, rec_lines in records:
        if rtype == 'INDI':
            individuals[rid] = rec_lines
            order.append((rid, 'INDI'))
        elif rtype == 'FAM':
            families[rid] = rec_lines
            order.append((rid, 'FAM'))
        else:
            # keep other records too
            order.append((rid, rtype))
    
    # build lookup info for individuals
    info = {}
    for rid, rec_lines in individuals.items():
        info[rid] = extract_individual_info(rec_lines)
    # merge individuals by same name+birth
    merge_map = {}
    canonical = {}
    for rid, (sur, giv, birth) in info.items():
        # require at least a surname and given name; birth may be missing
        if not (sur and giv):
            continue
        # treat missing birth as empty string so that two individuals
        # without dates but with identical names collapse as duplicates
        key = (sur.lower(), giv.lower(), birth or '')
        if key in canonical:
            merge_map[rid] = canonical[key]
        else:
            canonical[key] = rid
    # any rid not in merge_map is its own canonical
    # update references in family and individual records
    def canonical_ind(rid):
        return merge_map.get(rid, rid)
    # merge individual records by collecting additional lines
    for old, new in merge_map.items():
        # merge lines from old into new if not already present
        # skip the header (level 0) of the old record, it should not be
        # copied into the canonical record
        lines_to_copy = individuals[old][1:]
        for line in lines_to_copy:
            if line not in individuals[new]:
                individuals[new].append(line)
    # delete merged ones
    for old in merge_map.keys():
        individuals.pop(old, None)
    
    # rewrite references in individuals
    for rid, lines in individuals.items():
        new_lines = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 3 and parts[1] in ('FAMC','FAMS'):
                pid = parts[2]
                if pid.startswith('@'):
                    newpid = canonical_ind(pid)
                    if newpid != pid:
                        line = line.replace(pid, newpid)
            new_lines.append(line)
        individuals[rid] = new_lines
    # update family references to canonical individuals
    for fid, lines in list(families.items()):
        new_lines = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 3 and parts[1] in ('HUSB','WIFE','CHIL'):
                pid = parts[2]
                if pid.startswith('@'):
                    newpid = canonical_ind(pid)
                    if newpid != pid:
                        line = line.replace(pid, newpid)
            new_lines.append(line)
        families[fid] = new_lines

    # second pass: merge duplicate families
    def compute_fam_key(lines):
        husb = wife = None
        children = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 3:
                if parts[1] == 'HUSB':
                    husb = canonical_ind(parts[2])
                elif parts[1] == 'WIFE':
                    wife = canonical_ind(parts[2])
                elif parts[1] == 'CHIL':
                    children.append(canonical_ind(parts[2]))
        return (husb, wife, tuple(sorted(children)))

    fam_merge_map = {}
    changed = True
    while changed:
        changed = False
        seen = {}
        for fid, lines in families.items():
            key = compute_fam_key(lines)
            if key in seen:
                fam_merge_map[fid] = seen[key]
                # merge lines from the duplicate family into the canonical one
                # skip the level-0 header of the old record so we don't insert
                # a spurious "0 @OLD@ FAM" tag into the surviving record.
                for line in lines[1:]:
                    if line not in families[seen[key]]:
                        families[seen[key]].append(line)
                changed = True
            else:
                seen[key] = fid
        # delete merged ones
        for old, new in list(fam_merge_map.items()):
            if old in families and old != new:
                families.pop(old, None)
    
    # rewrite references to merged families in individuals
    def canonical_fam(fid):
        return fam_merge_map.get(fid, fid)
    for rid, lines in individuals.items():
        new_lines = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 3 and parts[1] in ('FAMC','FAMS'):
                pid = parts[2]
                if pid.startswith('@'):
                    newpid = canonical_fam(pid)
                    if newpid != pid:
                        line = line.replace(pid, newpid)
            new_lines.append(line)
        individuals[rid] = new_lines
    # rewrite references inside families too? families don't reference families.

    # before validation, remove duplicate labels within records
    def clean_duplicates(lines):
        """Remove duplicate occurrence of the same level+tag within a record."""
        seen = set()
        out = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 2:
                lvl = parts[0]
                tag = parts[1]
                key = (lvl, tag)
                if key in seen:
                    # skip duplicate
                    continue
                seen.add(key)
            out.append(line)
        return out

    # assemble all_records preserving order and cleaning duplicates
    all_records = []
    for rid, rtype in order:
        if rtype == 'INDI':
            if rid in individuals:
                cleaned = clean_duplicates(individuals[rid])
                all_records.append((rid, rtype, cleaned))
            # otherwise the individual was merged away; skip entirely
        elif rtype == 'FAM':
            if rid in families:
                cleaned = clean_duplicates(families[rid])
                all_records.append((rid, rtype, cleaned))
            # skipped families are duplicates merged away
        else:
            # preserve non‑INDI/FAM records exactly as read
            for r in records:
                if r[0] == rid and r[1] == rtype:
                    cleaned = clean_duplicates(r[2])
                    all_records.append((rid, rtype, cleaned))
                    break
    errors = validate_gedcom_records(all_records)
    if errors:
        sys.stderr.write("Validation errors:\n" + "\n".join(errors) + "\n")
    # write output
    with open(outfile, 'w', encoding='utf-8') as f:
        for rid, rtype, rec_lines in all_records:
            for line in rec_lines:
                f.write(line + '\n')


if __name__ == '__main__':
    main()
