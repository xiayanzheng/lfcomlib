class Numbers:

    def GenRange(self, StartNumber, EndNumber, GapNumber):
        NumberRangeResult = []
        RowNumberSP = StartNumber
        Gap = int(EndNumber) - int(StartNumber)
        if Gap > GapNumber:
            for X in range(int(Gap / GapNumber)):
                Temp = []
                Temp.append(RowNumberSP)
                Temp.append(RowNumberSP + GapNumber)
                NumberRangeResult.append(Temp)
                RowNumberSP += GapNumber
            Temp = []
            Temp.append(RowNumberSP)
            Temp.append(RowNumberSP + int(Gap % GapNumber))
            NumberRangeResult.append(Temp)
            RowNumberSP += int(Gap % GapNumber)
        else:
            NumberRangeResult.append([StartNumber, EndNumber])
        return NumberRangeResult