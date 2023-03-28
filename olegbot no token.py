import discord
from discord.ext import commands
import random
import asyncio #good luck figuring this shit out
import re #saved my life
import yt_dlp as youtube_dl
from discord import FFmpegPCMAudio
import os
import ytmusicapi

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.messages = True

bot = commands.Bot(command_prefix='/', intents=intents)

# jlpt dicts by level (only snippet of full dictionary for proof-of-concept)
N5 = {'日本語': 'Japanese', '英語': 'English', '電車': 'train, electric train', '鉛筆': 'pencil', '服': 'clothes',
      '灰皿': 'ashtray', '飛行機': 'aeroplane, airplane', '痛い': 'painful, sore', '辞書': 'dictionary', 'ここ': 'here',
      '毎月': 'every month', '耳': 'ear', '皆': 'all, everyone', '奥さん': 'wife, your wife, his wife', '歳': 'years old',
      '背': 'height, stature', '飛ぶ': 'to fly', '遠い': 'far, distant', 'とても': 'very, exceedingly', '売る': 'to sell',
      '横': 'horizontal, beside', '動物': 'animal', '二人': 'two people, pair',
      '二十日': 'twentieth day of the month, twenty days', '本当': 'truth, reality', '他': 'other, the rest',
      '自転車': 'bicycle', '家族': 'family, members of a family', '消える': 'to go out, to vanish',
      '前': 'front, ahead, previous', '見せる': 'to show, to display', '問題': 'question, problem',
      '難しい': 'difficult, hard', '鳴く': 'to sing', '押す': 'to push, to press', '男': 'man, male', '誕生日': 'birthday',
      '頼む': 'to request, to beg, to ask', '薄い': 'thin, pale, light', '八日': 'eight day of the month, eight days',
      '雑誌': 'journal, magazine', 'コップ': 'glass', '後': 'behind after, later', '出かける': 'to go out', 'どうも': 'thanks',
      '駅': 'station', '学校': 'school', '学生': 'student', '午前': 'morning, a.m.', '橋': 'bridge',
      '幾つ': 'how many, how old', '授業': 'lesson, class work'}
N4 = {'犬': 'dog', '猫': 'cat', '気分': 'feeling, mood', '首': 'neck', '空気': 'air, atmosphere',
      '億': 'hundred million', '将来': 'future, prospects', 'そろそろ': 'soon, momentarily', '多数': 'large number',
      '丁寧': 'polite, courteous, careful', '寺': 'temple', '受ける': 'to receive, to get', '沸かす': 'to boil, to heat',
      '夕食': 'evening meal, dinner', '地理': 'geography', '駐車場': 'parking lot', '電灯': 'electric light',
      '昼休み': 'lunch break', '一生懸命': 'very hard, with utmost effort', '神社': 'Shinto shrine',
      '関係': 'relation, relationship, connection', '顔': 'face, look', '国際': 'international',
      'この頃': 'recently, nowadays', '交通': 'traffic, transportation', '日記': 'diary, journal', '喉': 'throat',
      '屋上': 'rooftop', 'お礼': 'thanks, gratitude', '社会': 'society, public, community',
      '食料品': 'foodstuff, groceries', '包む': 'to wrap up, to tuck in', '笑う': 'to laugh',
      '優しい': 'tender, kind, gentle', '寄る': 'to approach, to drop by', '合う': 'to fit, to match, to suit',
      'どんどん': 'rapidly, continuously', '苛める': 'to bully, to torment', '急ぐ': 'to hurry, to rush',
      '会話': 'conversation', '怖い': 'scary, frightening', '真中': 'middle, center', '港': 'harbor, port',
      '戻る': 'to return, to go back', 'もし': 'if, in case', '迎える': 'to go out to meet', '匂い': 'scent, smell',
      'お祝い': 'congratulations, celebration', '可笑しい': 'funny, strange, odd', '親切': 'kindness, gentleness',
      '済む': 'to finish, to end', '届ける': 'to deliver, to send'}
N3 = {'建物': 'building', '食べ物': 'food', '基本': 'foundation, basis', '霧': 'fog, mist', '国民': 'national, citizen',
      '今回': 'now, this time', '好物': 'favourite food', '公平': 'fairness, justice', '工事': 'construction work',
      '航空': 'aviation, flying', '組み立てる': 'to assemble, to set up', '急速': 'rapid', '孫': 'grandchild',
      '味方': 'friend, ally', '燃える': 'to burn, to get fired up', '物語': 'tale, story', '眺め': 'view, scene, prospect',
      '値段': 'price, cost', '年中': 'whole year, all year round', '伸びる': 'to stretch, to extend',
      '能': 'talent, gift, function', '落ち着く': 'to calm down, to compose oneself', '思わず': 'unintentionally',
      '及ぼす': 'to exert, to cause', '例': 'example, case', '性': 'gender', '制度': 'system, institution',
      '正式': 'official, formality', '責める': 'to blame, to condemn', '節約': 'economizing, saving', '詩人': 'poet',
      '食器': 'tableware', '食料': 'food', '袖': 'sleeve', '全て': 'everything, all',
      '弾': 'ball, sphere, globe, bullet', '他人': 'another person, others', '誕生': 'birth, creation', '虎': 'tiger',
      '当日': 'appointed day, very day', '通学': 'commuting to school', '売り切れる': 'to be sold out',
      '脇': 'beside, close to, nearby', '割る': 'to divide, to cut', '喜び': 'joy, delight',
      '要素': 'element, factor, component', '稍': 'a little, partially', '温める': 'to warm, to heat',
      '微妙': 'delicate, subtle', '文': 'sentence', '分析': 'analysis', '中間': 'middle, midway, center'}
N2 = {'発表': 'announcement', '提案': 'proposal', '精一杯': 'best effort, with all ones might',
      '線路': 'railway track, railroad', '仕上げる': 'to finish up, to complete', '進入': 'entry, approach',
      '側面': 'side, flank, profile', '総合': 'synthesis, coordination', '住まい': 'dwelling, house',
      '辿り着く': 'to arrive at', '体質': 'constitution', '退職': 'retirement, resignation', '対等': 'equality',
      '転換': 'conversion, changeover', '溶かす': 'to dissolve, to melt', '取り組む': 'to grapple with, to engage in',
      '透明': 'transparent, clear', '強火': 'high flame', '喧しい': 'noisy, loud, clamorous',
      '寄せる': 'to bring near, to collect, to press', '要旨': 'point, essentials, summary', '郵送': 'mailing, posting',
      '溢れる': 'to overflow, to brim over', '空き地': 'vacant land, empty lot', '仰向け': 'face up',
      '洗い出す': 'to reveal, to bring to light', '改める': 'to change, to alter', '部員': 'staff, member',
      '分別': 'separation', '散らかす': 'to scatter around, to leave untidy', '抽象': 'abstraction',
      '段取り': 'program, plans, arrangements', '土台': 'foundation, base', '独占': 'monopoly, exclusivity',
      '複数': 'plural, multiple', '幅広い': 'extensive, wide, broad', '半日': 'half day',
      '引き渡す': 'to deliver, to hand over', '一人残らず': 'everyone', '本日': 'today', '表紙': 'cover',
      '著しい': 'striking, remarkable', '意欲': 'will, desire, ambition', '事物': 'things, affairs', '自体': 'itself',
      '塾': 'coaching school, cramming school', '順位': 'order, rank, position', '花粉': 'pollen',
      '改良': 'improvement, reform', '開店': 'opening a new shop', '欠かす': 'to miss', '下記': 'the following'}
N1 = {'動機付け': 'motivation', '調査': 'survey', '従業員': 'employee, worker',
      '経過': 'passage, expiration, progress',
      '奇跡': 'miracle, wonder, marvel',
      '究極': 'ultimate, extreme, final',
      '摸索': 'groping',
      '死': 'death, decease',
      '仕組み': 'structure, construction, arrangement, contrivance, mechanism, workings, plan, plot',
      '備わる': 'to be furnished with, to be equipped with',
      '退職': 'retirement, resignation',
      '勇敢': 'brave, heroic, gallant',
      '不動産': 'real estate',
      '封鎖': 'blockade',
      '把握': 'grasp, catch, understanding',
      '悲鳴': 'shriek, scream',
      '悲惨': 'disastrous, tragic',
      '実践': 'practice, putting into practice, implementation',
      '確信': 'conviction, belief, confidence',
      '効率': 'efficiency',
      '見方': 'viewpoint, point of view',
      '正義': 'justice, right, righteousness',
      '真理': 'truth',
      '真相': 'truth, real situation',
      '職務': 'professional duties',
      '促進': 'promotion, acceleration',
      '弱める': 'to weaken',
      '悪事': 'evil deed, crime',
      '扱い': 'treatment, service',
      '膨張': 'expansion, swelling, increase',
      '知性': 'intelligence',
      '忠実': 'faithful, devoted, loyal, honest, true',
      '腐敗': 'decomposition, corruption, decay',
      '負傷': 'injury, wound',
      '負担': 'burden, load, responsibility, bearing',
      '法廷': 'courtroom',
      '情熱': 'passion, enthusiasm',
      '賭ける': 'to wager, to bet, to gamble',
      '抗議': 'protest, objection',
      '恵む': 'to bless, to show mercy to, to give',
      '名誉': 'honor, credit, prestige',
      '無実': 'innocence, guiltlessness',
      '利息': 'interest',
      '察知': 'sense, infer',
      '衝動': 'impulse, impetus, urge',
      '手法': 'technique, method',
      '捜査': 'search, investigation',
      '展示': 'exhibition, display',
      '通常': 'usual, ordinary, normal, regular, general, common',
      '運用': 'making use of, application',
      '敏感': 'sensitive, alert, aware, susceptible',
      '部下': 'subordinate person',
      '建物': 'building',
      '食べ物': 'food',
      '基本': 'foundation, basis',
      '霧': 'fog, mist',
      '国民': 'national, citizen',
      '今回': 'now, this time',
      '好物': 'favorite food',
      '公平': 'fairness, justice',
      '工事': 'construction work',
      '航空': 'aviation, flying',
      '組み立てる': 'to assemble, to set up',
      '急速': 'rapid',
      '孫': 'grandchild',
      '味方': 'friend, ally'}

JLPT = {5: N5, 4: N4, 3: N3, 2: N2, 1: N1}

# dicts *DONT USE AS COMMAND NAMES*
studybook = {}
mastered = {}
learned = {}
timer = {}
correct_count = {}


# get random from studybook
def choose_random_word_from_studybook(user_id):
    studybook_data = get_from_studybook(user_id)
    return random.choice(list(studybook_data.items()))


async def search_song_on_youtube(ctx, word, artist=None, album=None, duration=None):
    ytmusic = ytmusicapi.YTMusic()
    search_results = ytmusic.search(word, filter="songs")

    # filters for getsong
    filtered_results = []
    for song in search_results:
        if artist and song['artists'][0]['name'] != artist:
            continue
        if album and song['album']['name'] != album:
            continue
        if duration and song['duration'] != duration:
            continue
        filtered_results.append(song)

    # gets the URL of the first song in the filtered results
    if filtered_results:
        video_id = filtered_results[0]['videoId']
        url = f"https://music.youtube.com/watch?v={video_id}"
    else:
        url = None

    return url


async def play_song_in_voice_channel(ctx, url):
    channel = ctx.author.voice.channel
    if channel is not None:
        voice_client = await channel.connect()

        # dl vid file
        ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'downloads/%(title)s.%(ext)s'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # play file 
        ffmpeg_executable = "ffmpeg"  
        voice_client.play(FFmpegPCMAudio(filename, executable=ffmpeg_executable))

        # wait audio end
        while voice_client.is_playing():
            await asyncio.sleep(1)

        # dc from vc and del file
        await voice_client.disconnect()
        os.remove(filename)
    else:
        await ctx.send("You need to be in a voice channel to play music.")


def get_from_studybook(user_id, default_value=None):
    if user_id not in studybook:
        return default_value or {}
    return studybook[user_id]


def jisho_link(word):
    return f"https://jisho.org/search/{word}"


@bot.command()
async def songn(ctx, level: str):
    if level not in ['1', '2', '3', '4', '5']:
        await ctx.send("Invalid JLPT level. Please choose a level between 1 and 5.")
        return

    word = get_word(f"N{level}")[0]  # Get a random word from the specified JLPT level
    url = await search_song_on_youtube(ctx, word)
    await ctx.send(f"Here's a JPop or Anime song with the word '{word}' in its title: {url}")
    await play_song_in_voice_channel(ctx, url)


@bot.command()
async def songfromstudybook(ctx):
    user_id = ctx.author.id
    word = choose_random_word_from_studybook(user_id)[0]
    url = await search_song_on_youtube(ctx, word)
    await ctx.send(f"Here's a JPop or Anime song with the word '{word}' from your study book in its title: {url}")
    await play_song_in_voice_channel(ctx, url)


# command list here zzzzz (inaccurate descriptions until i can be bothered to change)
@bot.command()
async def helpme(ctx):
    embed = discord.Embed(
        title="Japanese Study Bot Commands",
        description=(
            "A list of all the available commands and their brief explanations:\n\n"
            "/newn5, /newn4, /newn3, /newn2, /newn1 - Sends a word in Japanese from levels N5-N1 respectively, "
            "with a link to jisho.org\n\n "
            "/mystudybook - Displays all words added to the user's studybook\n\n"
            "/settimer - Sets a timer for initiating a review session\n\n"
            "/timerstatus - Displays the remaining time on the timer\n\n"
            "/endtimer - Ends the currently running timer\n\n"
            "/review 5, /review 4, /review 3, /review 2, /review 1 - Initiates a review session of the words in your studybook for levels N5-N1 respective\n\n"
            "/wipe - Wipes the user's studybook\n\n"
            "/masteredwords - Displays the user's mastered words\n\n"
            "/learnedwords - Displays the words the user has correctly reviewed\n\n"
            "/songn5, /songn4, /songn3, /songn2, /songn1 - Sends a random JP song with random word from specified level in title\n\n"
            "/songfromstudybook - Sends a random JP song with random word from your studybook in the title\n\n"
            "Contact oleg#1357 on Discord if you encounter any issues."
        )
    )
    await ctx.send(embed=embed)


# get rndm word from dict.
def get_word(level):
    return random.choice(list(JLPT[level].items()))


# newn5
@bot.command()
async def newn5(ctx):
    user_id = ctx.author.id
    used_words = set(get_from_studybook(user_id, {}).keys()) if user_id in studybook else set()
    unused_words = set(N5.keys()) - used_words
    if len(unused_words) == 0:
        await ctx.send("You have already learned all the words in the N5 list.")
    else:
        word = random.choice(list(unused_words))
        meaning = N5[word]
        await send_word(ctx, word, meaning)


# mirrors of newn5
@bot.command()
async def newn4(ctx):
    await new_word_at_level(ctx, 4)


@bot.command()
async def newn3(ctx):
    await new_word_at_level(ctx, 3)


@bot.command()
async def newn2(ctx):
    await new_word_at_level(ctx, 2)


@bot.command()
async def newn1(ctx):
    await new_word_at_level(ctx, 1)


async def new_word_at_level(ctx, level):
    user_id = ctx.author.id
    used_words = set(get_from_studybook(user_id, {}).keys()) if user_id in studybook else set()
    unused_words = set(JLPT[level].keys()) - used_words
    if len(unused_words) == 0:
        await ctx.send(f"You have already learned all the words in the N{level} list.")
    else:
        word = random.choice(list(unused_words))
        meaning = JLPT[level][word]
        await send_word(ctx, word, meaning)


# sends new word, sends to studybook or discards on reply
async def send_word(ctx, word, meaning):
    jisho_url = jisho_link(word)
    message = f"New word to learn: {word}\n{jisho_url}\n\nReply with 'y' if you want this word to be added to your " \
              f"studybook, reply with 'n' if not. "
    await ctx.send(message)

    def check_message(message):
        return message.author == ctx.author and message.content.lower() in ['y', 'n']

    try:
        response = await bot.wait_for('message', timeout=30.0, check=check_message)
        if response.content.lower() == 'y':
            if ctx.author.id not in studybook:
                studybook[ctx.author.id] = {}
            studybook[ctx.author.id][word] = meaning
            await ctx.send(f"{word} has been added to your studybook!")
        else:
            await ctx.send(f"{word} has been discarded.")
    except asyncio.TimeoutError:
        await ctx.send("You took too long to decide. The word has been discarded.")


@bot.command()
async def mystudybook(ctx):
    user_id = ctx.author.id
    if user_id not in studybook or not studybook[user_id]:
        await ctx.send("Your studybook is empty! Use /newnX commands to add words.")
    else:
        await ctx.send("Your studybook contains the following words:\n" + ", ".join(studybook[user_id].keys()))


timer_tasks = {}


async def timer_callback(ctx, user_id, duration, time_unit):
    await asyncio.sleep(duration)
    await ctx.send(
        f"<@!{user_id}>, {duration} {time_unit} have surpassed. Time for your review session! Reply with /check and "
        f"let's see how well you remember your vocab.")


class TimerTask(asyncio.Task):
    def __init__(self, coro, duration, *, loop=None, name=None):
        super().__init__(coro, loop=loop, name=name)
        self.start_time = loop.time() if loop else asyncio.get_event_loop().time()
        self.duration = duration

    def time_remaining(self):
        elapsed_time = (asyncio.get_event_loop().time() - self.start_time)
        return max(0, self.duration - elapsed_time)


async def timer_callback(ctx, user_id, duration, unit):
    await asyncio.sleep(duration)
    await ctx.send(f"{ctx.author.mention}, time's up! Your {duration} {unit} timer has ended.")
    timer_tasks.pop(user_id, None)


def parse_duration(duration_str):
    # DISCARD THIS SHIT ASAP
    match = re.match(r'(?:(?P<hours>\d+)\s*hour(s?)\s*)?(?:(?P<minutes>\d+)\s*minute(s?)\s*)?$', duration_str)
    if not match:
        return None

    hours = int(match.group('hours') or 0)
    minutes = int(match.group('minutes') or 0)

    if hours > 24 or (hours == 24 and minutes > 0):
        return None

    return hours * 3600 + minutes * 60


@bot.command()
async def settimer(ctx):
    def check_message(message):
        return message.author == ctx.author

    await ctx.send("Please enter how long you would like the timer to be set for in the format 'duration unit' (e.g. "
                   "10 minutes, 2 hours) \n Unforunately, I don't yet support combinations of units :(")

    try:
        duration_text = await bot.wait_for('message', check=check_message, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. The timer has not been set.")
        return

    try:
        duration = parse_duration(duration_text.content)
    except ValueError as e:
        await ctx.send(str(e))
        return

    if duration > 24 * 60 * 60:
        await ctx.send("The maximum duration is 24 hours.")
        return

    if duration < 60:
        await ctx.send("The minimum duration is 1 minute.")
        return

    unit = 'seconds' if duration < 60 else 'minutes' if duration < 60 * 60 else 'hours'

    if unit == 'hours':
        await ctx.send(
            f"わかった！See you in {duration / 3600} {unit}. Of course you may force a review session before then using the /review commands. \n Use the command /timerstatus at any time to check how long is "
            f"remaining or /endtimer if you made a mistake.")
    if unit == 'minutes':
        await ctx.send(
            f"わかった！See you in {duration / 60} {unit}. Of course you may force a review session before then using the /review commands. \n Use the command /timerstatus at any time to check how long is "
            f"remaining or /endtimer if you made a mistake.")

        user_id = ctx.author.id
        timer_tasks[user_id] = TimerTask(timer_callback(ctx, user_id, duration, unit), duration)


@bot.command()
async def timerstatus(ctx):
    user_id = ctx.author.id
    if user_id not in timer_tasks or timer_tasks[user_id].done():
        await ctx.send("There is no active timer. Use /settimer to create a new one.")
    else:
        remaining_time = timer_tasks[user_id].time_remaining()
        hours, remainder = divmod(remaining_time, 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours > 0:
            await ctx.send(f"There are {hours} hour(s) {minutes} minute(s) remaining on your timer.")
        elif minutes > 0:
            await ctx.send(f"There are {minutes} minute(s) {seconds} second(s) remaining on your timer.")
        else:
            await ctx.send(f"There are {seconds} second(s) remaining on your timer.")


@bot.command()
async def endtimer(ctx):
    user_id = ctx.author.id
    if user_id in timer_tasks and not timer_tasks[user_id].done():
        timer_tasks[user_id].cancel()
        await ctx.send("Your timer has been canceled. Use /settimer to create a new one.")
    else:
        await ctx.send("There is no active timer to cancel. Use /settimer to create a new one.")


def check_response(m, ctx):
    return m.author == ctx.author and m.channel == ctx.channel


JLPT = {5: N5, 4: N4, 3: N3, 2: N2, 1: N1}


def get_word_level(word):
    for level in JLPT:
        if word in JLPT[level]:
            return level
    return None


async def review_question(ctx, word):
    level = get_word_level(word)
    if level is None:
        await ctx.send(f"Sorry, I don't have the translation for '{word}' in my JLPT dictionaries.")
        return False

    translations = JLPT[level][word].split(',')
    translations = [t.strip().lower() for t in translations]
    await ctx.send(f"Reply with the translation of this word: **{word}** and I'll check if you're right!")
    response = await bot.wait_for('message', check=lambda m: check_response(m, ctx))
    user_response = response.content.strip().lower()

    if user_response in translations:
        await ctx.send(f"Correct! Well done. {jisho_link(word)}")
        return True
    else:
        await ctx.send(f"Incorrect. The correct translation{'s are' if len(translations) > 1 else ' is'} "
                       f"{', '.join(translations)}. {jisho_link(word)}")
        return False


@bot.command()
async def review(ctx, level: int):
    user_id = ctx.author.id
    if user_id not in correct_count or user_id not in studybook or not studybook[user_id]:
        studybook[user_id] = {word: 0 for word in studybook[user_id]}
    if user_id not in studybook or len(studybook[user_id]) == 0:
        await ctx.send("Your studybook is empty. Add words to your studybook using /newn5, /newn4, /newn3, /newn2, "
                       "or /newn1.")
    else:
        words_to_review = {word: studybook[user_id][word] for word in studybook[user_id] if
                           get_word_level(word) == level}
        if len(words_to_review) == 0:
            await ctx.send(f"No words to review for JLPT N{level}.")
            return

        while len(words_to_review) > 0:
            word = random.choice(list(words_to_review.keys()))
            correct = await review_question(ctx, word)

            if correct:
                correct_count.setdefault(user_id, {})
                correct_count[user_id][word] = correct_count[user_id].get(word, 0) + 1
                if correct_count[user_id][word] >= 10:
                    if user_id not in mastered:
                        mastered[user_id] = []
                    if word not in mastered[user_id]:
                        mastered[user_id].append(word)
                del words_to_review[word]
                studybook[user_id][word] = max(studybook[user_id][word] - 1, 0)
            else:
                await ctx.send(
                    "Reply with 'next word' to move on to the next word, or 'terminate' to end the review session.")
                response = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
                if response.content.lower() == 'next word':
                    continue
                elif response.content.lower() == 'terminate':
                    await ctx.send("Review session terminated.")
                    return
                else:
                    await ctx.send("Invalid input. Session terminated.")
                    return
        await ctx.send("All words reviewed for JLPT N{level}.")


@bot.command()
async def wipe(ctx):
    user_id = ctx.author.id
    await ctx.send("Are you really sure you wish to wipe your studybook? Doing so will mean you "
                   "have to add all words again. Reply 'YES' if you're sure or anything else to cancel the request.")
    try:
        response = await bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.send("Time out! Request cancelled")
    else:
        if response.content.lower() == 'yes':
            studybook[user_id] = {}
            await ctx.send("かしこまりました！Your studybook is now empty.")
        else:
            await ctx.send("わかった！I won't touch your studybook. Hope this won't also be true for you!")


@bot.command()
async def masteredwords(ctx):
    user_id = ctx.author.id
    if user_id not in mastered or len(mastered[user_id]) == 0:
        await ctx.send("You have yet display to me your mastery of any words from your studybook! Get reviewing!")
    else:
        mastered_list = ", ".join(mastered[user_id])
        await ctx.send(f"You have mastered the following word(s): {mastered_list} \n 上手ですね！")


@bot.command()
async def learnedwords(ctx):
    user_id = ctx.author.id
    if user_id not in correct_count or len(correct_count[user_id]) == 0:
        await ctx.send("You have yet to learn any words from your studybook! Get reviewing!")
    else:
        learned_words_msg = "You have correctly reviewed the following points at some point:\n"
        for word, count in correct_count[user_id].items():
            learned_words_msg += f"{word}: {count} times\n"
        await ctx.send(learned_words_msg)


@bot.event #displays msg as bot's current activity
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='/helpme for command list'))
    print('Bot is ready.')      

      
# random rock-paper-scissors game xd
async def get_choice(user, dm_channel):
    def check(m):
        return m.author == user and m.channel == dm_channel and m.content.upper() in ['R', 'P', 'S']

    try:
        message = await bot.wait_for('message', timeout=30, check=check)
        return message.content.upper()
    except asyncio.TimeoutError:
        return None


async def determine_winner(choice1, choice2, user1, user2, ctx):
    if choice1 == choice2:
        return None
    if (choice1 == 'R' and choice2 == 'S') or (choice1 == 'P' and choice2 == 'R') or (
            choice1 == 'S' and choice2 == 'P'):
        return user1
    return user2


@bot.command()
async def rps(ctx, user2: discord.Member):
    user1 = ctx.author

    if user1 == user2:
        await ctx.send("Damn, didn't realise you are that lonely.\n You could technically challenge yourself to "
                       "rock-paper-scissors, but I'd prefer you go make some friends")
        return

    dm_channel1 = await user1.create_dm()
    dm_channel2 = await user2.create_dm()

    await dm_channel1.send(
        "Reply with R for rock, P for paper, or S for scissors. You have 30 seconds to make a choice!")
    await dm_channel2.send(
        "Reply with R for rock, P for paper, or S for scissors. You have 30 seconds to make a choice!")
    await ctx.send("You have 30 seconds to make a choice!")

    round_number = 1
    winner = None

    while winner is None:
        choice1 = await get_choice(user1, dm_channel1)
        choice2 = await get_choice(user2, dm_channel2)

        if choice1 is None and choice2 is None:
            await ctx.send("No responses retrieved, game terminated")
            return

        if choice1 is None:
            winner = user2
            await ctx.send(f"{user1.mention} was too slow! {user2.mention} won.")
            return

        if choice2 is None:
            winner = user1
            await ctx.send(f"{user2.mention} was too slow! {user1.mention} won.")
            return

        winner = await determine_winner(choice1, choice2, user1, user2, ctx)

        if winner is None:
            await ctx.send(f"Round {round_number} ended in a draw! You have 30 seconds to send another choice.")
            round_number += 1
        else:
            await ctx.send(
                f"Responses received, revealing results below...\n||{user1.mention} chose {choice1}, {user2.mention} chose {choice2}. {winner.mention} won!||")


bot.run("my private bot token")
