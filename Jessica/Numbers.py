class Numbers:

    def gen_range(self, StartNumber, EndNumber, GapNumber):
        number_range_result = []
        row_number_sp = StartNumber
        gap = int(EndNumber) - int(StartNumber)
        if gap > GapNumber:
            for X in range(int(gap / GapNumber)):
                temp = []
                temp.append(row_number_sp)
                temp.append(row_number_sp + GapNumber)
                number_range_result.append(temp)
                row_number_sp += GapNumber
            temp = []
            temp.append(row_number_sp)
            temp.append(row_number_sp + int(gap % GapNumber))
            number_range_result.append(temp)
            row_number_sp += int(gap % GapNumber)
        else:
            number_range_result.append([StartNumber, EndNumber])
        return number_range_result
