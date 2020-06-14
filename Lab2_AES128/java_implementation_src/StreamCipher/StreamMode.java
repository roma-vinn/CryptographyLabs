package StreamCipher;

import java.util.Arrays;

public class StreamMode {
    static int[][] arrToMatrix(int[] arr) {
        assert arr.length == 16;
        int[][] martix = new int[4][4];
        for (int i = 0; i < 4; i++) {
            System.arraycopy(arr, 4 * i, martix[i], 0, 4);
        }

        return martix;
    }

    static int[] matrixToArr(int[][] matrix) {
        assert matrix.length == 4 && matrix[0].length == 4;
        int[] arr = new int[16];
        for (int i = 0; i < 4; i++) {
            System.arraycopy(matrix[i], 0, arr, 4 * i, 4);
        }
        return arr;
    }

    static int[][] matrixXOR(int[][] a, int[][] b) {
        assert a.length == b.length && a[0].length == b[0].length;

        int[][] c = new int[a.length][a[0].length];

        for (int i = 0; i < a.length; i++) {
            for (int j = 0; j < a[0].length; j++) {
                c[i][j] = a[i][j] ^ b[i][j];
            }
        }
        return c;
    }

    public static void main(String[] args) {
        // test
        int[] test_arr = new int[16];

        for (int i = 0; i < 16; i++) {
            test_arr[i] = i+1;
        }

        int[][] test_matrix = arrToMatrix(test_arr);

        for (int i = 0; i < 4; i++) {
            System.out.println(Arrays.toString(test_matrix[i]));
        }

        System.out.println(Arrays.toString(matrixToArr(test_matrix)));
    }
}
