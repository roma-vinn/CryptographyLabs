package StreamCipher;

import AES.AES;

import java.util.Arrays;


public class CBC extends StreamMode {
    private static int N = 16;  // block length

    private static int[] encrypt(int[] plainText, int[][] key) {
        assert plainText.length % N == 0;  // without padding

        int n_blocks = plainText.length / N;
        int[] encrypted = new int[plainText.length];
        AES cipher = new AES();
        int[][] ci = new int[N/4][N/4];  // initial value = zeros

        for (int i = 0; i < n_blocks; i++) {
            int[] curBlock = Arrays.copyOfRange(plainText, N * i, N * (i + 1));
            ci = cipher.encrypt(matrixXOR(ci, arrToMatrix(curBlock)), key);
            System.arraycopy(matrixToArr(ci), 0, encrypted, N*i, N);
        }

        return encrypted;
    }

    private static int[] decrypt(int[] cipherText, int[][] key) {
        assert cipherText.length % N == 0;  // without padding

        int n_blocks = cipherText.length / N;
        int[] decrypted = new int[cipherText.length];
        AES cipher = new AES();
        int[][] ci = new int[N/4][N/4];  // initial value = zeros
        int[][] mi;

        for (int i = 0; i < n_blocks; i++) {
            int[] curBlock = Arrays.copyOfRange(cipherText, N * i, N * (i + 1));
            mi = matrixXOR(cipher.decrypt(arrToMatrix(curBlock), key), ci);
            ci = arrToMatrix(curBlock);
            System.arraycopy(matrixToArr(mi), 0, decrypted, N*i, N);
        }

        return decrypted;

    }


    public static void main(String[] args) {
        int[][] key = new int[4][4];
        int[] arr = new int[32];

        for (int i = 0; i < 32; i++) {
            arr[i] = i;
        }
        // CBC test
        System.out.println(Arrays.toString(encrypt(arr, key)));
        System.out.println(Arrays.toString(decrypt(encrypt(arr, key), key)));

    }
}
