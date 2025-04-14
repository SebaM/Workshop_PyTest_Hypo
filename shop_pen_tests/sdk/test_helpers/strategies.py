import uuid

from hypothesis.strategies._internal.core import characters, sampled_from, composite
from hypothesis import settings, Verbosity
import datetime
from hypothesis import strategies as st

# Define a strategy for generating strings with leading or trailing whitespace

HYPOTHESIS_DEFAULT_SETTINGS = dict(
    verbosity=Verbosity.normal,
    deadline=datetime.timedelta(seconds=30),
    max_examples=30
)

def leading_trailing_whitespace_strategy(**kwargs):
    # Generate random text
    text = st.text(**kwargs, alphabet=characters(codec="ascii", exclude_categories=['M', 'P', 'S', 'Z', 'C']))
    # Generate leading and trailing whitespace
    whitespace = st.text(alphabet=characters(codec="ascii", categories=['Z']), min_size=1, max_size=10)
    # trailing_whitespace = st.text(alphabet=" \t\n\r", min_size=1, max_size=10)
    # Combine them into a string with leading and trailing whitespace
    return st.builds(
        lambda lw, t, tw: f"{lw}{t}{tw}",
        whitespace,
        text,
        whitespace
    )


# Reqs:
# ad:12:13:fc:14:ee // 48 bit, with colons
# ad-12-13-fc-14-ee // 48 bit, with dashes
# ad1213fc14ee      // 48 bit, without any delimiter
# AD:12:13:FC:14:EE // 48 bit, uppercase.
# 001A.2B3C.4D5E
#
# AD:12:13:FC:14:EE:FF:FF // 64 bit, uppercase
# ad:12:13:fc:14:ee:13:ad // 64 bit, lowercase
# ad-12-13-fc-14-ee-ff-ad // 64 bit, with dashes
# ad1213fc14eeffae        // 64 bit, without any delimter
def mac_colon_strategy():
    return st.from_regex(r"([0-9A-F]{2}[:]){5}([0-9A-F]{2})", fullmatch=True)


def mac_colon_strategy_48bits():
    return st.from_regex(r"([0-9A-F]{2}[:]){7}([0-9A-F]{2})", fullmatch=True)


def mac_dash_strategy():
    return st.from_regex(r"([0-9A-F]{2}[-]){5}([0-9A-F]{2})", fullmatch=True)


def mac_dash_strategy_48bits():
    return st.from_regex(r"([0-9A-F]{2}[-]){7}([0-9A-F]{2})", fullmatch=True)


def mac_dot_strategy():
    return st.from_regex(r"([0-9A-F]{4}[.]){2}([0-9A-F]{4})", fullmatch=True)


def mac_no_breaks_strategy():
    return st.from_regex(r"[0-9A-F]{12}", fullmatch=True)


def mac_no_breaks_strategy48():
    return st.from_regex(r"[0-9A-F]{16}", fullmatch=True)


def mac_strategy():
    # full list according IEEE802
    # return st.one_of(mac_colon_strategy(), mac_colon_strategy_48bits(), mac_dash_strategy(), mac_dash_strategy_48bits(),
    #                      mac_dot_strategy(), mac_no_breaks_strategy(), mac_no_breaks_strategy48())
    return st.one_of(mac_colon_strategy(), mac_dash_strategy(), mac_dot_strategy())

# Example usage:
# example_strategy = leading_trailing_whitespace_strategy()
# example_strategy.example()  # Generates a random string with leading/trailing whitespace



@composite
def allowed_name_strategy(draw):
    base = draw(st.from_regex(r'[a-zA-Z0-9-_:. ()]{50,218}', fullmatch=True))  # allow space for suffix
    suffix = str(uuid.uuid4())
    return f"{base}-{suffix}"


def random_name_strategy():
    return st.text(min_size=1, max_size=255)


def allowed_update_name_strategy():
    return st.builds(
        lambda suffix: 'UPDATED-' + suffix,
        st.from_regex(r'[a-zA-Z0-9-_:. ()]{1,247}', fullmatch=True))


def long_name_strategy():
    return st.from_regex(r'[a-zA-Z0-9-_:. ()]{256}', fullmatch=True)


def invalid_name_strategy():
    """
    Generates random invalid name using strategies:
    I. long_name_strategy
    II. random_name_strategy.filter(lambda s: not s.strip()
        - generates random strings,
        - narrows down the generated strings to those that match the condition: lambda s: not s.strip()
        - where "s.strip()" removes all leading and trailing whitespace.
        - If the result is an empty string (""), then "not s.strip()" is True.
        - So strings like " ", "\n\t ", etc. are also generated.
        """
    return  long_name_strategy() | random_name_strategy().filter(lambda s: not s.strip())


def whitespace_name_strategy():
    return  st.text(alphabet=st.just(" "), min_size=1, max_size=255)


def edge_case_names():
    return st.sampled_from([
    "\n",       # newline
    "\t",       # tab
    "\r\n",     # Windows newline
    "!",        # punctuation
    "   ",      # multiple spaces
    ".",        # dot
    ":",        # colon
    "  \t \n ", # mixed whitespace
    " MUG",        # leading space
    "MUG ",        # trailing space
    "MUG    ",     # trailing multiple
    " MUG ",       # both leading and trailing
    "\tMUG",     # leading tab
    "MUG\n",     # trailing newline
    "  MUG  ",     # multiple on both sides
])
