import mido
from mido import Message, MidiFile, MidiTrack
import time

class SimpleScorePlayer:
    def __init__(self, tempo=120, program=0, velocity=64):
        self.tempo = tempo  # BPM
        self.ticks_per_beat = 480  # MIDI 时间分辨率
        self.program = program  # MIDI 音色
        self.velocity = velocity  # MIDI 力度
        self.note_duration = self.ticks_per_beat // 2  # 默认八分音符
        self.mid = MidiFile()
        self.track = MidiTrack()
        
        # 简谱数字到MIDI音符的映射 (C大调)
        self.note_map:dict[str, int] = {
            '0': 0,   # 休止符
            '|': 0,   # 休止符
            '1': 60,  # C4 (do)
            '2': 62,  # D4 (re)
            '3': 64,  # E4 (mi)
            '4': 65,  # F4 (fa)
            '5': 67,  # G4 (sol)
            '6': 69,  # A4 (la)
            '7': 71,  # B4 (si)
            
            '1.': 48, # C3 (低八度do)
            '2.': 50, # D3 (低八度re)
            '3.': 52, # E3 (低八度mi)
            '4.': 53, # F3 (低八度fa)
            '5.': 55, # G3 (低八度sol)
            '6.': 57, # A3 (低八度la)
            '7.': 59, # B3 (低八度si)

            '1^': 72, # C5 (高八度do)
            '2^': 74, # D5 (高八度re)
            '3^': 76, # E5 (高八度mi)
            '4^': 77, # F5 (高八度fa)
            '5^': 79, # G5 (高八度sol)
            '6^': 81, # A5 (高八度la)
            '7^': 83, # B5 (高八度si)

            '-': self.ticks_per_beat * 2,  # 二分音符
            ' ': self.ticks_per_beat,      # 四分音符
            '`': self.ticks_per_beat // 2, # 八分音符
            '_': self.ticks_per_beat // 4  # 十六分音符
        }
    
    def parse_score(self, score_str:str):
        """解析简谱字符串"""
        # 支持空格或逗号分隔的音符
        notes = score_str.replace(',', ' ').split()
        return notes
    
    def create_midi(self, notes:list[str|int]|str, output_file='output.mid'):
        """根据音符列表创建MIDI文件"""
        self.mid.tracks.append(self.track)
        
        # 设置音色 (0是钢琴)
        self.track.append(Message('program_change', program=self.program, time=0))
        
        # 设置速度
        tempo = mido.bpm2tempo(self.tempo)
        self.track.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))
        
        # 添加音符
        for note in notes:
            note = str(note)
            if note in self.note_map:
                midi_note = self.note_map[note]
                if midi_note > 0:  # 不是休止符
                    self.track.append(Message('note_on', note=midi_note, velocity=self.velocity, time=0))
                    self.track.append(Message('note_off', note=midi_note, velocity=self.velocity, time=self.note_duration))
                else:  # 休止符
                    self.track.append(Message('note_off', note=0, velocity=0, time=self.note_duration))
            elif '~' in note: #连音符
                overlap = self.note_duration // 2
                midi_note=self.note_map[note.replace('~', '')]
                self.track.append(Message('note_on', note=midi_note, velocity=self.velocity, time=0))
                self.track.append(Message('note_off', note=midi_note, velocity=self.velocity, time=overlap))
        
        # 保存文件
        self.mid.save(output_file)
        return self.mid
    
    def play_score(self, score_str:str):
        """播放简谱"""
        notes = self.parse_score(score_str)
        mid = self.create_midi(notes, 'temp.mid')
        
        try:
            # 尝试播放MIDI
            with mido.open_output() as port:
                for msg in mid.play():
                    port.send(msg)
        except:
            print("无法播放MIDI，请检查MIDI输出设备")
            print(f"已生成MIDI文件: temp.mid")

# 使用示例
if __name__ == "__main__":
    player = SimpleScorePlayer(tempo=120)
    
    # 示例简谱 ("小星星"前两句)
    score = "1 1 5 5 6 6 5 0 4 4 3 3 2 2 1"
    print(f"演奏简谱: {score}")
    player.play_score(score)