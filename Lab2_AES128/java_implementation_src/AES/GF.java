package AES;

import java.util.Arrays;

public class GF {
    int num;
    private static int modulo = 0x011b;

    GF(int decimal){
        this.num = decimal;
    }

    // addition == bitwise XOR
    static GF add(GF a, GF b){
        return new GF(a.num ^ b.num);
    }

    // mul
    static GF mul(GF a, GF b){
        int res = 0;
        for (int i = 0; i < 8; ++i){
            if (((1 << i) & b.num) != 0){
                int tmp = a.num;
                for (int j = 0; j < i; ++j){
                    tmp = tmp << 1;
                    if (tmp >= 256){
                        tmp = tmp ^ GF.modulo;
                    }
                }
                res = res ^ tmp;
            }
        }
        return new GF(res);
    }

    @Override
    public String toString(){
        String res = Integer.toHexString(this.num);
        if (res.length() == 1){
            res = "0" + res;
        }
        return "0x" + res;
    }

    public static void main(String[] args){
        GF[] tmp = new GF[2];
        tmp[0] = new GF(255);
        tmp[1] = new GF(12);
        System.out.println(Arrays.toString(tmp));
        System.out.println(GF.add(tmp[0], tmp[1]));
        System.out.println(GF.mul(tmp[0], tmp[1]));

        GF[] test = new GF[6];
        test[0] = new GF(2);
        test[1] = new GF(3);
        test[2] = new GF(0xd4);
        test[3] = new GF(0xbf);
        test[4] = new GF(0x5d);
        test[5] = new GF(0x30);
        GF res = GF.add(GF.add(GF.mul(test[0], test[2]), GF.mul(test[1], test[3])),
                GF.add(test[4], test[5]));
        System.out.println(res);
    }
}