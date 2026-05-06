from linked_list import DoublyLinkedList, Track, Playlist, BrowserHistory

passed = 0
failed = 0

def test(name, got, expected):
    global passed, failed
    if got == expected:
        print(f"  ✓  {name}")
        passed += 1
    else:
        print(f"  ✗  {name}")
        print(f"       expected: {expected!r}")
        print(f"       got:      {got!r}")
        failed += 1

def test_true(name, condition):
    test(name, condition, True)

def test_raises(name, fn, error_type):
    global passed, failed
    try:
        fn()
        print(f"  ✗  {name}  (no exception raised)")
        failed += 1
    except error_type:
        print(f"  ✓  {name}")
        passed += 1
    except Exception as e:
        print(f"  ✗  {name}  (wrong exception: {e})")
        failed += 1


print("\n── DoublyLinkedList ──────────────────────────────────")

dll = DoublyLinkedList()
test("empty list has length 0", len(dll), 0)
test("is_empty on new list", dll.is_empty(), True)

dll.append("A")
dll.append("B")
dll.append("C")
test("length after 3 appends", len(dll), 3)
test("iterate forward", list(dll), ["A", "B", "C"])
test("head is A", dll.head.data, "A")
test("tail is C", dll.tail.data, "C")
test("contains A", "A" in dll, True)
test("does not contain Z", "Z" in dll, False)

dll.prepend("Z")
test("prepend puts Z at head", dll.head.data, "Z")
test("length after prepend", len(dll), 4)
test("iterate after prepend", list(dll), ["Z", "A", "B", "C"])

dll.insert_after("A", "X")
test("insert_after A gives X", list(dll), ["Z", "A", "X", "B", "C"])

dll.remove("X")
test("remove X", list(dll), ["Z", "A", "B", "C"])
dll.remove("Z")
test("remove head Z", list(dll), ["A", "B", "C"])
dll.remove("C")
test("remove tail C", list(dll), ["A", "B"])
test("tail updated after remove", dll.tail.data, "B")

test_raises("remove missing raises ValueError",
            lambda: dll.remove("NOT_HERE"), ValueError)
test_raises("insert_after missing raises ValueError",
            lambda: dll.insert_after("NOT_HERE", "X"), ValueError)


print("\n── Track ─────────────────────────────────────────────")

t1 = Track("Blinding Lights", "The Weeknd", 200)
t2 = Track("Levitating", "Dua Lipa", 203)
t3 = Track("Blinding Lights", "The Weeknd", 200)

test("track str contains title",   "Blinding Lights" in str(t1), True)
test("track str contains artist",  "The Weeknd"      in str(t1), True)
test("track str contains duration","3:20"             in str(t1), True)
test("equal tracks",   t1 == t3, True)
test("unequal tracks", t1 == t2, False)


print("\n── Playlist ──────────────────────────────────────────")

pl = Playlist("Test Playlist")
pl.add(t1)
pl.add(t2)
test("now playing after add", pl.now_playing, t1)

t4 = Track("Stay", "The Kid LAROI", 141)
pl.add_next(t4)
pl.next_track()
test("next track is the queued one", pl.now_playing, t4)

pl.previous_track()
test("previous goes back", pl.now_playing, t1)

result = pl.next_track()
test("next_track returns the track", result, t4)


print("\n── BrowserHistory ────────────────────────────────────")

bh = BrowserHistory("https://google.com")
bh.visit("https://github.com")
bh.visit("https://python.org")
test("current page", bh.current_page(), "https://python.org")

bh.back()
test("back once", bh.current_page(), "https://github.com")
bh.back()
test("back twice", bh.current_page(), "https://google.com")
test("back from start returns None", bh.back(), None)

bh.forward()
test("forward once", bh.current_page(), "https://github.com")

bh.visit("https://docs.python.org")
test("new visit clears forward", bh.current_page(), "https://docs.python.org")
test("forward after new visit returns None", bh.forward(), None)


print(f"\n{'═'*45}")
print(f"  {passed} passed  |  {failed} failed")
print(f"{'═'*45}\n")
