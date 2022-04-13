InterruptIn start_button(p5);
InterruptIn human_done(p6);
DigitalOut led(p7);
int tiles_available = 100;
volatile bool can_make_word = True;


void start_game() {
    deal_ai_tiles(7);
    deal_human_tiles(7);

}

void ai_turn() {
    led = 0;
    // ai can make a word or skip
    if (can_make_word) {
        // word formation mechanics
        word_length = ai_play_word();
        deal_tiles(word_length, ai);

    } else {    // skipping turn
        led = 1;
        human_turn();
    }
}

void human_turn() {
    if (can_make_word) {
        // human makes word and presses button, interrupt in main will trigger
        word_length = word_tracking_function();
        deal_tiles(word_length, human);
    }
}

int ai_play_word() {
    // playing word function
    return word_length
}

void deal_tiles(int num_tiles, char player) {
    tiles_available -= num_tiles;
    // tile distribution mechanics
    if (player == ai) {
        // deal to ai
    } else {
        // deal to human
    }
}

void game_over() {
    // return tiles back to storage mechanics
}

int main() {
    start_button.rise(&start_game);
    human_done.rise(&ai_turn)
    while (tiles_available > 0 && can_make_word) {
        // chill here
    }
    game_over();
}